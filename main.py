import subprocess
import sys
import os

# Gerekli kütüphaneleri otomatik yükle
def install_packages():
    packages = ['pytelegrambotapi', 'requests']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"📦 {package} yükleniyor...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_packages()

# Şimdi ana kodu çalıştır
import telebot
import time
import threading
import random
import string
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8469749003:AAGYW2tPh-IjHfGfO5ufdyQmTpGLcH9tew8"
bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = "https://t.me/addlist/DtLDoLd26skyODQ9"  # Kanal kullanıcı adı

# Admin ID'leri
ADMIN_IDS = [7945410079]  # Buraya kendi ID'nizi ve diğer adminleri ekleyin

# Telegram boş mesaj kabul etmez → görünür güvenli metin
TEXT = "FAKE NO GENERATOR HOŞGELDİNİZ\nKANALLARA GİRİP DEVAM EDİNİZ"

# Ülke kodları
PREFIX = {
    "TR": "+90",
    "IN": "+91",
    "PT": "+351",
    "PL": "+48",
    "IL": "+972"
}

# Kullanıcı puanları ve referansları
user_points = {}
user_referrals = {}

# JSON dosya adı
JSON_FILE = "fakeno.json"

# JSON dosyasını yükle
def load_data():
    global user_points, user_referrals
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_points = data.get('points', {})
                user_referrals = data.get('referrals', {})
                # String anahtarları integere çevir
                user_points = {int(k): v for k, v in user_points.items()}
                user_referrals = {int(k): v for k, v in user_referrals.items()}
        except:
            user_points = {}
            user_referrals = {}
    else:
        user_points = {}
        user_referrals = {}

# JSON dosyasını kaydet
def save_data():
    data = {
        'points': user_points,
        'referrals': user_referrals
    }
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Kanal kontrolü
def check_channel_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Admin kontrolü
def is_admin(user_id):
    return user_id in ADMIN_IDS

# Kanal katılma butonu
def get_channel_button():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📢 KANALA KATIL", url=f"https://t.me/laedrisystems"))
    kb.add(InlineKeyboardButton("✅ KATILDIM KONTROL ET", callback_data="check_channel"))
    return kb

# Türkiye operatör-benzeri prefixler (5XX)
TR_PREFIX = [
    "530","531","532","533","534","535","536","537","538","539",
    "540","541","542","543","544","545","546","547","548","549",
    "550","551","552","553","554","555","556","557","558","559"
]

def get_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def send_otp_with_delay(chat_id, message_id, otp_type, number):
    """10 saniye bekleyip OTP'yi gönder"""
    time.sleep(10)
    
    if otp_type == "wa":
        # WhatsApp OTP
        whatsapp_otp = generate_whatsapp_otp()
        random_code = get_random_string(12)
        
        msg = (
            f"<#> WhatsApp kod: {whatsapp_otp}\n"
            f"Kodu paylaşmayın\n"
            f"{random_code}"
        )
        bot.send_message(chat_id, msg)
        
    else:
        # Telegram OTP
        telegram_otp = generate_telegram_otp()
        
        msg = (
            f"Giriş kodu: {telegram_otp}. Telegram'dan olduklarını söyleseler bile bu kodu kimseyle paylaşmayın!\n\n"
            f"❗️Bu kod, Telegram hesabınızda oturum açmak için kullanılabilir. Bunun dışında başka bir şey istemiyoruz.\n\n"
            f"Başka bir cihazda oturum açmaya çalışarak bu kodu istemediyseniz, bu mesajı dikkate almayın."
        )
        bot.send_message(chat_id, msg)

@bot.message_handler(commands=["start"])
def start(m):
    args = m.text.split()
    user_id = m.from_user.id
    
    # Kanal kontrolü - İLK ÖNCE KANAL KONTROLÜ YAP
    if not check_channel_member(user_id):
        bot.send_message(
            m.chat.id, 
            "❌ Önce kanala katılmalısınız!",
            reply_markup=get_channel_button()
        )
        return
    
    # KANAL KONTROLÜ GEÇTİYSE, şimdi referans kontrolü yap
    referrer_gave_point = False
    
    # Referans kontrolü
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])
        # Kendine referans verme ve daha önce referans verilmemiş mi kontrolü
        if referrer_id != user_id and user_id not in user_referrals.get(referrer_id, []):
            
            # Referans kaydet
            if referrer_id not in user_referrals:
                user_referrals[referrer_id] = []
            user_referrals[referrer_id].append(user_id)
            
            # Referans puanı ekle (SADECE KANAL KONTROLÜ GEÇTİĞİ İÇİN)
            if referrer_id not in user_points:
                user_points[referrer_id] = 0
            user_points[referrer_id] += 1
            
            # JSON kaydet
            save_data()
            referrer_gave_point = True
            
            # Referans kazanan kullanıcıya mesaj gönder
            try:
                bot.send_message(
                    referrer_id,
                    f"🎉 Tebrikler! Yeni bir referans kazandınız!\n"
                    f"📊 Toplam puanınız: {user_points[referrer_id]}"
                )
            except:
                pass
    
    # Yeni kullanıcıyı kaydet (daha önce kayıtlı değilse)
    if user_id not in user_points:
        user_points[user_id] = 0
        save_data()
    
    # Ana menüyü göster
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📢 KANAL", url="https://t.me/laedrisystems"))
    kb.add(InlineKeyboardButton("✅ GİRDİM", callback_data="g"))
    bot.send_message(m.chat.id, TEXT, reply_markup=kb)
    
    # Referans puanı verildiyse bilgi mesajı
    if referrer_gave_point:
        bot.send_message(
            m.chat.id,
            "✅ Referans başarıyla kaydedildi! Arkadaşınıza puan eklendi."
        )

@bot.callback_query_handler(func=lambda c: c.data == "check_channel")
def check_channel(c):
    user_id = c.from_user.id
    if check_channel_member(user_id):
        bot.edit_message_text(
            "✅ Kanal kontrolü başarılı! Devam edebilirsiniz.",
            c.message.chat.id,
            c.message.message_id
        )
        time.sleep(1)
        # Ana menüyü göster
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("📢 KANAL", url="https://t.me/laedrisystems"))
        kb.add(InlineKeyboardButton("✅ GİRDİM", callback_data="g"))
        bot.send_message(c.message.chat.id, TEXT, reply_markup=kb)
    else:
        bot.answer_callback_query(
            c.id,
            "❌ Kanala katılmadınız! Önce katılın.",
            show_alert=True
        )

def open_menu(chat_id, msg_id, user_id):
    time.sleep(random.randint(1, 2))
    
    # Kanal kontrolü
    if not check_channel_member(user_id):
        bot.edit_message_text(
            "❌ Kanaldan çıkmışsınız! Lütfen tekrar katılın.",
            chat_id, 
            msg_id,
            reply_markup=get_channel_button()
        )
        return
    
    points = user_points.get(user_id, 0)
    
    kb = InlineKeyboardMarkup(row_width=1)
    
    # Ülke butonları
    kb.add(
        InlineKeyboardButton(f"🇹🇷 TÜRKİYE {f'[{points}]' if points > 0 else ''}", callback_data="TR"),
        InlineKeyboardButton(f"🇮🇳 HİNDİSTAN {f'[{points}]' if points > 0 else ''}", callback_data="IN"),
        InlineKeyboardButton(f"🇵🇹 PORTEKİZ {f'[{points}]' if points > 0 else ''}", callback_data="PT"),
        InlineKeyboardButton(f"🇵🇱 POLONYA {f'[{points}]' if points > 0 else ''}", callback_data="PL"),
        InlineKeyboardButton(f"🇮🇱 İSRAİL {f'[{points}]' if points > 0 else ''}", callback_data="IL"),
    )
    
    # Referans linki butonu
    kb.add(InlineKeyboardButton("🔗 REFERANS BİLGİLERİM", callback_data="ref_info"))
    
    bot.edit_message_text(
        f"🌍 Ülke Seçin\n📊 Puanınız: {points}\n🔗 Referansla puan kazanın!",
        chat_id, 
        msg_id, 
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data == "g")
def girdim(c):
    user_id = c.from_user.id
    
    # Kanal kontrolü
    if not check_channel_member(user_id):
        bot.edit_message_text(
            "❌ Kanala katılmadınız!",
            c.message.chat.id,
            c.message.message_id,
            reply_markup=get_channel_button()
        )
        return
    
    bot.edit_message_text(TEXT, c.message.chat.id, c.message.message_id)
    threading.Thread(
        target=open_menu,
        args=(c.message.chat.id, c.message.message_id, user_id),
        daemon=True
    ).start()

@bot.callback_query_handler(func=lambda c: c.data == "ref_info")
def referans_bilgileri(c):
    user_id = c.from_user.id
    points = user_points.get(user_id, 0)
    referrals = len(user_referrals.get(user_id, []))
    
    # Bot username'ini al
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    
    # Referans bilgileri mesajı
    ref_msg = (
        f"🔗 **REFERANS BİLGİLERİNİZ**\n\n"
        f"💰 Mevcut Puanınız: {points}\n"
        f"👥 Toplam Referans: {referrals}\n\n"
        f"📋 **Referans Linkiniz:**\n"
        f"`{ref_link}`\n\n"
        f"📌 **Nasıl Çalışır?**\n"
        f"• Linki arkadaşlarınızla paylaşın\n"
        f"• Arkadaşınız kanala katılıp botu başlatsın\n"
        f"• Size otomatik +1 puan eklenir\n"
        f"• 2 puanla OTP alabilirsiniz\n\n"
        f"👇 Linki kopyalamak için tıklayın"
    )
    
    # Kopyalama butonlu keyboard
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📋 Linki Kopyala", callback_data=f"copy_{ref_link}"))
    kb.add(InlineKeyboardButton("🔙 Geri Dön", callback_data="g"))
    
    bot.edit_message_text(
        ref_msg,
        c.message.chat.id,
        c.message.message_id,
        reply_markup=kb,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("copy_"))
def copy_link(c):
    link = c.data[5:]  # copy_ sonrası link
    # Kullanıcıya linki göster
    bot.answer_callback_query(
        c.id,
        "✅ Link hazır! Kopyalamak için basılı tutun.",
        show_alert=False
    )
    # Linki ayrı bir mesaj olarak gönder
    bot.send_message(
        c.message.chat.id,
        f"📋 **Referans Linkiniz:**\n`{link}`",
        parse_mode="Markdown"
    )

def fake_number(country):
    if country == "TR":
        prefix = random.choice(TR_PREFIX)
        rest = ''.join(str(random.randint(0, 9)) for _ in range(7))
        return "+90" + prefix + rest
    else:
        return PREFIX[country] + ''.join(str(random.randint(0, 9)) for _ in range(9))

def generate_whatsapp_otp():
    first = random.randint(100, 999)
    second = random.randint(100, 999)
    return f"{first}-{second}"

def generate_telegram_otp():
    return random.randint(10000, 99999)

def otp_flow(chat_id, country, user_id):
    # Puan kontrolü
    points = user_points.get(user_id, 0)
    
    if points < 2:
        bot.send_message(
            chat_id,
            f"❌ Yetersiz puan!\n"
            f"📊 Mevcut puanınız: {points}\n"
            f"⚡️ 2 puan gerekiyor.\n"
            f"🔗 Referans vererek puan kazanın!"
        )
        return
    
    # Önce numarayı gönder
    number = fake_number(country)
    bot.send_message(chat_id, f"📱 Numara: {number}\n✅ Ülke: {country}")
    
    # 10 saniye bekle
    time.sleep(10)
    
    # İnline butonlar
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📱 WhatsApp'a Attım", callback_data=f"wa_{number}"),
        InlineKeyboardButton("✈️ Telegram'a Attım", callback_data=f"tg_{number}")
    )
    
    bot.send_message(
        chat_id,
        "📲 Kodu nereye gönderdiniz?",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("wa_") or c.data.startswith("tg_"))
def otp_callback(c):
    user_id = c.from_user.id
    number = c.data[3:]  # wa_ veya tg_ sonrası numara
    otp_type = "wa" if c.data.startswith("wa_") else "tg"
    
    # Puan düş
    if user_points.get(user_id, 0) >= 2:
        user_points[user_id] -= 2
        save_data()
    
    # "Kod çıkartılıyor..." mesajını gönder
    bot.edit_message_text(
        "🔄 Kod çıkartılıyor... Lütfen bekleyin (10 saniye)",
        c.message.chat.id,
        c.message.message_id
    )
    
    # 10 saniye sonra OTP'yi gönderecek thread'i başlat
    threading.Thread(
        target=send_otp_with_delay,
        args=(c.message.chat.id, c.message.message_id, otp_type, number),
        daemon=True
    ).start()

@bot.callback_query_handler(func=lambda c: c.data in ["TR","IN","PT","PL","IL"])
def country_select(c):
    user_id = c.from_user.id
    
    # Kanal kontrolü
    if not check_channel_member(user_id):
        bot.answer_callback_query(
            c.id,
            "❌ Kanala katılmadınız!",
            show_alert=True
        )
        return
    
    threading.Thread(
        target=otp_flow,
        args=(c.message.chat.id, c.data, user_id),
        daemon=True
    ).start()

@bot.message_handler(commands=["duyuru"])
def duyuru_gonder(m):
    # Sadece admin kullanabilir
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Bu komutu kullanma yetkiniz yok!")
        return
    
    # Duyuru mesajını al
    duyuru_metni = m.text.replace("/duyuru", "").strip()
    if not duyuru_metni:
        bot.reply_to(m, "❌ Duyuru metni girin!\nÖrnek: /duyuru Merhaba arkadaşlar...")
        return
    
    # Tüm kullanıcılara gönder
    basarili = 0
    basarisiz = 0
    
    status_msg = bot.reply_to(m, "📨 Duyuru gönderiliyor...")
    
    for user_id in user_points.keys():
        try:
            bot.send_message(
                user_id,
                f"📢 **DUYURU**\n\n{duyuru_metni}\n\n-- Fake No Generator",
                parse_mode="Markdown"
            )
            basarili += 1
            time.sleep(0.05)  # Rate limit koruması
        except:
            basarisiz += 1
    
    # Sonuç mesajı
    bot.edit_message_text(
        f"✅ Duyuru gönderimi tamamlandı!\n\n"
        f"📨 Başarılı: {basarili}\n"
        f"❌ Başarısız: {basarisiz}\n"
        f"👥 Toplam: {len(user_points)}",
        status_msg.chat.id,
        status_msg.message_id
    )

@bot.message_handler(commands=["puanver"])
def puan_ver(m):
    # Sadece admin kullanabilir
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Bu komutu kullanma yetkiniz yok!")
        return
    
    # Komut formatını kontrol et: /puanver <kullanici_id> <puan>
    args = m.text.split()
    if len(args) != 3:
        bot.reply_to(
            m, 
            "❌ Yanlış format!\n"
            "Doğru kullanım: `/puanver 123456789 5`\n"
            "📝 Not: Puan sayısı pozitif tam sayı olmalıdır.",
            parse_mode="Markdown"
        )
        return
    
    try:
        hedef_kullanici = int(args[1])
        eklenecek_puan = int(args[2])
        
        if eklenecek_puan <= 0:
            bot.reply_to(m, "❌ Puan sayısı pozitif olmalıdır!")
            return
        
        # Kullanıcıyı kaydet (yoksa)
        if hedef_kullanici not in user_points:
            user_points[hedef_kullanici] = 0
        
        # Puan ekle
        user_points[hedef_kullanici] += eklenecek_puan
        save_data()
        
        # Başarılı mesajı
        bot.reply_to(
            m,
            f"✅ Başarılı!\n\n"
            f"👤 Kullanıcı: `{hedef_kullanici}`\n"
            f"💰 Eklenen Puan: `{eklenecek_puan}`\n"
            f"📊 Yeni Toplam: `{user_points[hedef_kullanici]}`",
            parse_mode="Markdown"
        )
        
        # Hedef kullanıcıya bildirim gönder
        try:
            bot.send_message(
                hedef_kullanici,
                f"🎁 **Hediye Puan Kazandınız!**\n\n"
                f"💰 Hesabınıza `{eklenecek_puan}` puan eklendi.\n"
                f"📊 Yeni puanınız: `{user_points[hedef_kullanici]}`\n\n"
                f"-- Fake No Generator",
                parse_mode="Markdown"
            )
        except:
            bot.send_message(
                m.chat.id,
                "⚠️ Hedef kullanıcıya mesaj gönderilemedi (botu başlatmamış olabilir)."
            )
            
    except ValueError:
        bot.reply_to(m, "❌ Geçersiz ID veya puan formatı!")
    except Exception as e:
        bot.reply_to(m, f"❌ Bir hata oluştu: {str(e)}")

@bot.message_handler(commands=["puan"])
def puan_sorgula(m):
    user_id = m.from_user.id
    points = user_points.get(user_id, 0)
    referrals = len(user_referrals.get(user_id, []))
    
    # Bot username'i al
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔗 Referans Linkim", url=ref_link))
    
    bot.reply_to(
        m,
        f"📊 **Puan Durumunuz**\n\n"
        f"💰 Puanınız: {points}\n"
        f"👥 Referanslarınız: {referrals}\n\n"
        f"🔗 Referans Linkiniz hazır! Butona tıklayın.",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["adminhelp"])
def admin_help(m):
    if not is_admin(m.from_user.id):
        bot.reply_to(m, "❌ Bu komutu kullanma yetkiniz yok!")
        return
    
    help_text = (
        "👑 **ADMIN KOMUTLARI**\n\n"
        "📢 `/duyuru <mesaj>` - Tüm kullanıcılara duyuru gönder\n"
        "💰 `/puanver <id> <puan>` - Kullanıcıya hediye puan ver\n"
        "📊 `/puan` - Kendi puanınızı görüntüleyin\n"
        "🆘 `/adminhelp` - Bu yardım mesajını göster\n\n"
        "📝 **Örnekler:**\n"
        "• `/duyuru Yeni güncelleme!`\n"
        "• `/puanver 123456789 5`"
    )
    
    bot.reply_to(m, help_text, parse_mode="Markdown")

# JSON yükle
load_data()

# Botu başlat
print("🤖 Bot başlatılıyor...")
print(f"📁 JSON dosyası: {JSON_FILE}")
print(f"👥 Kayıtlı kullanıcı: {len(user_points)}")
print(f"👑 Admin ID: {ADMIN_IDS}")
print(f"📢 Kanal Kontrol: {CHANNEL_USERNAME}")
bot.infinity_polling()

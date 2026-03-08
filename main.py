import telebot
from telebot import types
import json
import os
from datetime import datetime
import time

TOKEN = "8234388592:AAEaplt1NV1t4MRvAXaunI5-RS5HXNmXA00"
bot = telebot.TeleBot(TOKEN)

# Zorunlu kanallar
ZORUNLU_KANALLAR = [
    {
        "link": "https://t.me/+ge40DY3JKhc0Y2Yy",
        "id": -1003590768175
    }
]
# === KONTROL FONKSİYONU ===
def kanallarda_mi(user_id):

    for kanal in ZORUNLU_KANALLAR:
        try:
            member = bot.get_chat_member(kanal["id"], user_id)
            
            if member.status not in ["member", "administrator", "creator"]:
                return False

        except Exception as e:
            print(f"Kanal kontrol hatası: {kanal['id']} | {e}")
            return False

    return True

# === START KOMUTU GÜNCELLEMESİ ===

URUNLER = {
        "pubg_hesap": {
            "ad": "🎮 Pubg Hesap",
            "fiyat": 10,
            "aciklama": "PUBG hesap teslim edilir."
        },
    "tiktok_hit": {
        "ad": "🔥 Tiktok Hit",
        "fiyat": 5,
        "aciklama": "Tiktok videonuz için etkileşim."
    },
    "wp_no": {
        "ad": "💬 Wp No",
        "fiyat": 12,
        "aciklama": "WhatsApp onaylı numara."
    },
    "tg_no": {
        "ad": "✈️ Tg No",
        "fiyat": 20,
        "aciklama": "Telegram onaylı numara."
    },
    "cpm_kesin": {
        "ad": "📈 Cpm Kesin",
        "fiyat": 5,
        "aciklama": "CPM garantili hizmet."
    },
    "insta_eski": {
        "ad": "📸 İnsta Eski Kurulum",
        "fiyat": 7,
        "aciklama": "Eski kurulum Instagram hesabı."
    },
    "tiktok_yuksek_hit": {
        "ad": "🚀 Tiktok 2-10k Hit",
        "fiyat": 15,
        "aciklama": "Tiktok için yüksek hit gönderimi."
    },
    "wp_cekme_bot": {
        "ad": "🤖 Sınırsız Wp Çekme Bot",
        "fiyat": 17,
        "aciklama": "Sınırsız WhatsApp numara çekme botu."
    },
    "100_emoji": {
        "ad": "🎭 100 Emoji",
        "fiyat": 10,
        "aciklama": "100 adet emoji etkileşimi."
    },
    "pubg_buzdiyari": {
        "ad": "❄️ Pubg Buzdiyarı Random",
        "fiyat": 15,
        "aciklama": "Buzdiyarı garantili veya şanslı random hesap."
    },
    "blutv_giris": {
        "ad": "📺 Blutv Kesin Giriş",
        "fiyat": 8,
        "aciklama": "Kesin giriş garantili BluTV hesabı."
    },
    "exxen_giris": {
        "ad": "🎬 Exxen Kesin Giriş",
        "fiyat": 5,
        "aciklama": "Kesin giriş garantili Exxen hesabı."
    },
    "netflix": {
        "ad": "🎥 Netflix",
        "fiyat": 6,
        "aciklama": "Netflix izleme profili/hesabı."
    },
    "valorant": {
        "ad": "🔫 Valorant",
        "fiyat": 10,
        "aciklama": "Valorant random hesap teslimi."
    },

    # Yeni eklenenler
    "live_civciv": {
        "ad": "🐥 Live Civciv",
        "fiyat": 10,
        "aciklama": "Canlı civciv hizmeti."
    },
    "idefix_hit": {
        "ad": "📚 İdefix Hit",
        "fiyat": 5,
        "aciklama": "İdefix için hit gönderimi."
    },
    "disney_plus": {
        "ad": "🎬 Disney+",
        "fiyat": 5,
        "aciklama": "Disney+ hesap/profil erişimi."
    },
    "pubg_uc": {
        "ad": "💎 Pubg UC",
        "fiyat": 8,
        "aciklama": "PUBG UC teslim edilir."
    }
}# === VERİ DOSYALARI ===
if not os.path.exists("kullanicilar.json"):
    with open("kullanicilar.json", "w") as f:
        json.dump({}, f)

def load_users():
    try:
        with open("kullanicilar.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("kullanicilar.json", "w") as f:
        json.dump(data, f, indent=4)

# === GRUP KONTROLÜ ===
def grupta_mi(user_id):
    try:
        member = bot.get_chat_member(ZORUNLU_GRUP_ID, user_id)
        return member.status in ['member','administrator','creator']
    except:
        return False
# === KULLANICI OLUŞTUR ===
def ensure_user(uid, username=None, first_name=None):
    data = load_users()
    if uid not in data:
        data[uid] = {
            "puan": 0,
            "referans_veren": None,
            "referans_getirdigi": [],
            "referans_sayisi": 0,
            "username": username or "",
            "isim": first_name or "",
            "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "son_aktif": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "grup_kontrol": False,
            "satin_aldiklari": []
        }
        save_users(data)
    else:
        # Son aktif güncelle
        data[uid]["son_aktif"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username:
            data[uid]["username"] = username
        if first_name:
            data[uid]["isim"] = first_name
        save_users(data)
    return data[uid]

# === ANA MENÜ ===
def ana_menu(chat_id, yeni_kullanici=False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Ürün butonları
    for urun_id, urun in URUNLER.items():
        markup.add(types.InlineKeyboardButton(
            f"{urun['ad']} - {urun['fiyat']}💰", 
            callback_data=f"urun_{urun_id}"
        ))
    
    # Alt butonlar
    markup.add(
        types.InlineKeyboardButton("💰 Puan Durumu", callback_data="puan_durumu"),
        types.InlineKeyboardButton("📨 Referans Linkim", callback_data="ref_link")
    )
    markup.add(
        types.InlineKeyboardButton("📢 Gruba Katıl", url=ZORUNLU_GRUP_LINK),
        types.InlineKeyboardButton("👤 Admin @Hakikiyetsiz", url=f"https://t.me/{YENI_ADMIN_USERNAME}")
    )
    
    if yeni_kullanici:
        bot.send_message(
            chat_id,
            "🎉 **Hoş Geldin!**\n\n"
            "Aşağıdaki ürünlerden satın alabilirsin:\n"
            "📊 10 Tepki = 1 Puan\n"
            "👥 50 Üye = 5 Puan\n"
            "👁️ Mesaj Görüntüleme = 5 Puan\n\n"
            "⬇️ Butonları kullanarak işlem yapabilirsin:",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            chat_id,
            "🏠 **Ana Menü**\n\n"
            "⬇️ İşlem seç:",
            reply_markup=markup,
            parse_mode="Markdown"
        )

# === /start ===
@bot.message_handler(commands=["start"])
def start(message):
    uid = str(message.from_user.id)
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    
    # Referans kontrolü
    args = message.text.split()
    referans_id = None
    
    if len(args) > 1:
        referans_id = args[1]
        if referans_id == uid:
            referans_id = None
    
    # Kullanıcıyı oluştur
    ensure_user(uid, username, first_name)
    data = load_users()
    
  # GRUP KONTROLÜ - İlk startta mutlaka kontrol et
if not grupta_mi(uid):
    # Gruba katılmamış
    markup = types.InlineKeyboardMarkup()

    grup_link = ZORUNLU_KANALLAR[0]["link"]

    markup.add(types.InlineKeyboardButton("📢 Gruba Katıl", url=grup_link))
    markup.add(types.InlineKeyboardButton("✅ Katıldım Kontrol Et", callback_data="grup_kontrol"))

    bot.send_message(
        uid,
        "⚠️ **ZORUNLU GRUP**\n\n"
        "Bu botu kullanabilmek için önce aşağıdaki gruba katılmalısın:\n\n"
        f"👉 {grup_link}\n\n"
        "**Katıldıktan sonra** '✅ Katıldım Kontrol Et' butonuna bas.",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    return
    
    # Referans işlemi
    if referans_id and data.get(uid) and data[uid].get("referans_veren") is None:
        # Referans verene puan ekle
        ref_id = str(referans_id)
        if ref_id in data:
            # Puan ve sayı artırma
            data[ref_id]["puan"] = data[ref_id].get("puan", 0) + 1
            data[ref_id]["referans_sayisi"] = data[ref_id].get("referans_sayisi", 0) + 1
            
            # Listeye ekleme
            if "referans_getirdigi" not in data[ref_id]:
                data[ref_id]["referans_getirdigi"] = []
            data[ref_id]["referans_getirdigi"].append(uid)
            
            # Kullanıcıyı işaretle (tekrar puan vermesin)
            data[uid]["referans_veren"] = ref_id

            # Referans verene bildirim gönder
            try:
                mesaj = (
                    f"🎉 **Yeni Referans Kazandın!**\n\n"
                    f"👤 {first_name} (@{username}) senin referansınla katıldı!\n"
                    f"💰 +1 Puan kazandın!\n"
                    f"📊 Toplam referansın: {data[ref_id]['referans_sayisi']}"
                )
                bot.send_message(ref_id, mesaj, parse_mode="Markdown")
            except Exception as e:
                print(f"Bildirim gönderilemedi: {e}")

        
        # Yeni kullanıcıya da hoşgeldin puanı (1 puan)
        data[uid]["puan"] = data[uid].get("puan", 0) + 1
        data[uid]["referans_veren"] = referans_id
        save_users(data)
        
        # Ana menüyü göster (yeni kullanıcı mesajıyla)
        ana_menu(uid, yeni_kullanici=True)
    else:
        # Normal giriş
        ana_menu(uid)

# === GRUP KONTROL CALLBACK ===
@bot.callback_query_handler(func=lambda call: call.data == "grup_kontrol")
def grup_kontrol_callback(call):
    uid = str(call.from_user.id)
    
    if grupta_mi(uid):
        bot.answer_callback_query(call.id, "✅ Gruba katılmışsın! Devam edebilirsin.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        ana_menu(uid)
    else:
        bot.answer_callback_query(call.id, "❌ Hala gruba katılmadın!", show_alert=True)

# === ÜRÜN SATIN ALMA ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("urun_"))
def urun_sec(call):
    uid = str(call.from_user.id)
    urun_id = call.data.replace("urun_", "")
    
    if urun_id not in URUNLER:
        bot.answer_callback_query(call.id, "❌ Ürün bulunamadı!")
        return
    
    urun = URUNLER[urun_id]
    data = load_users()
    user_data = data.get(uid, {"puan": 0})
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✅ Onayla", callback_data=f"onayla_{urun_id}"),
        types.InlineKeyboardButton("❌ İptal", callback_data="ana_menu_don")
    )
    
    bot.edit_message_text(
        f"📦 **{urun['ad']}**\n\n"
        f"{urun['aciklama']}\n\n"
        f"💰 Fiyat: {urun['fiyat']} Puan\n"
        f"📊 Mevcut Puanın: {user_data.get('puan', 0)}\n\n"
        f"Satın almayı onaylıyor musun?",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("onayla_"))
def urun_onayla(call):
    uid = str(call.from_user.id)
    urun_id = call.data.replace("onayla_", "")
    
    if urun_id not in URUNLER:
        bot.answer_callback_query(call.id, "❌ Ürün bulunamadı!")
        return
    
    urun = URUNLER[urun_id]
    data = load_users()
    
    if uid not in data:
        bot.answer_callback_query(call.id, "❌ Kullanıcı bulunamadı!")
        return
    
    if data[uid]["puan"] < urun["fiyat"]:
        bot.answer_callback_query(call.id, f"❌ Yetersiz puan! Gerekli: {urun['fiyat']}", show_alert=True)
        return
    
    # Puanı düş
    data[uid]["puan"] -= urun["fiyat"]
    data[uid]["satin_aldiklari"] = data[uid].get("satin_aldiklari", []) + [{
        "urun": urun["ad"],
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fiyat": urun["fiyat"]
    }]
    save_users(data)
    
    # Adminlere bildirim
    for admin in ADMINLER:
        try:
            admin_markup = types.InlineKeyboardMarkup()
            admin_markup.add(types.InlineKeyboardButton(
                f"👤 @{data[uid].get('username', 'Kullanıcı')}", 
                url=f"tg://user?id={uid}"
            ))
            
            bot.send_message(
                admin,
                f"🛒 **YENİ SATIN ALMA**\n\n"
                f"👤 Kullanıcı: {data[uid].get('isim', '')} (@{data[uid].get('username', 'yok')})\n"
                f"🆔 ID: `{uid}`\n"
                f"📦 Ürün: {urun['ad']}\n"
                f"💰 Fiyat: {urun['fiyat']} Puan\n"
                f"⏰ Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                reply_markup=admin_markup,
                parse_mode="Markdown"
            )
        except:
            pass
    
    # Kullanıcıya onay mesajı
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Ürün Teslim", url=f"https://t.me/{YENI_ADMIN_USERNAME}"))
    markup.add(types.InlineKeyboardButton("🏠 Ana Menü", callback_data="ana_menu_don"))
    
    bot.edit_message_text(
        f"✅ **Satın Alma Başarılı!**\n\n"
        f"📦 {urun['ad']}\n"
        f"💰 Ödenen: {urun['fiyat']} Puan\n"
        f"📊 Kalan Puan: {data[uid]['puan']}\n\n"
        f"📞 Ürün teslimi için @{YENI_ADMIN_USERNAME} ile iletişime geç!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id, "✅ Satın alındı!")

# === DİĞER CALLBACKLER ===
@bot.callback_query_handler(func=lambda call: call.data == "puan_durumu")
def puan_durumu(call):
    uid = str(call.from_user.id)
    data = load_users()
    user_data = data.get(uid, {"puan": 0, "referans_sayisi": 0, "kayit_tarihi": "bilinmiyor"})
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏠 Ana Menü", callback_data="ana_menu_don"))
    
    bot.edit_message_text(
        f"💰 **Puan Durumun**\n\n"
        f"📊 Puan: `{user_data.get('puan', 0)}`\n"
        f"👥 Referans Sayısı: `{user_data.get('referans_sayisi', 0)}`\n"
        f"🆔 ID: `{uid}`\n"
        f"📅 Kayıt: {user_data.get('kayit_tarihi', 'bilinmiyor')}\n\n"
        f"📦 Satın Aldıkların: {len(user_data.get('satin_aldiklari', []))} ürün",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "ref_link")
def ref_link(call):
    uid = str(call.from_user.id)
    ref_link = f"https://t.me/{BOT_USERNAME}?start={uid}"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📱 Paylaş", url=f"https://t.me/share/url?url={ref_link}"),
        types.InlineKeyboardButton("🏠 Ana Menü", callback_data="ana_menu_don")
    )
    
    bot.edit_message_text(
        f"📨 **Senin Referans Linkin:**\n\n"
        f"`{ref_link}`\n\n"
        f"Bu linki paylaş, her katılan için **+1 puan** kazan!\n"
        f"Not: Katılanlar gruba katılmazsa puan gelmez.",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "ana_menu_don")
def ana_menu_don(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    ana_menu(call.message.chat.id)
    bot.answer_callback_query(call.id)

# === ADMIN PANELİ ===
@bot.message_handler(commands=["adminpaneli"])
def admin_panel(message):
    uid = str(message.from_user.id)
    
    if uid not in ADMINLER:
        bot.reply_to(message, "❌ Bu komutu kullanma yetkin yok!")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Tüm Kullanıcılar", callback_data="admin_kullanicilar"),
        types.InlineKeyboardButton("💰 Puan Sıralaması", callback_data="admin_siralama"),
        types.InlineKeyboardButton("📢 Duyuru Gönder", callback_data="admin_duyuru"),
        types.InlineKeyboardButton("📦 Son Satın Almalar", callback_data="admin_satinalmalar")
    )
    
    data = load_users()
    toplam_kullanici = len(data)
    toplam_puan = sum([k.get("puan", 0) for k in data.values()])
    
    bot.send_message(
        uid,
        f"👑 **Admin Paneli**\n\n"
        f"📊 Toplam Kullanıcı: {toplam_kullanici}\n"
        f"💰 Toplam Puan: {toplam_puan}\n"
        f"👤 Admin: @{YENI_ADMIN_USERNAME}\n\n"
        f"⬇️ İşlem seç:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_kullanicilar")
def admin_kullanicilar(call):
    uid = str(call.from_user.id)
    
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "❌ Yetkin yok!")
        return
    
    data = load_users()
    
    # Son 10 kullanıcıyı göster
    mesaj = "📊 **Son Kayıt Olan Kullanıcılar:**\n\n"
    
    # Tarihe göre sırala
    kullanicilar = sorted(
        data.items(), 
        key=lambda x: x[1].get("kayit_tarihi", ""), 
        reverse=True
    )[:10]
    
    for k, v in kullanicilar:
        mesaj += f"👤 @{v.get('username', 'yok')} | {v.get('isim', '')}\n"
        mesaj += f"🆔 `{k}` | 💰 {v.get('puan', 0)} puan\n"
        mesaj += f"📅 {v.get('kayit_tarihi', '')}\n"
        mesaj += "─" * 20 + "\n"
    
    mesaj += f"\n📊 Toplam: {len(data)} kullanıcı"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Geri", callback_data="admin_geri"))
    
    bot.edit_message_text(
        mesaj,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_siralama")
def admin_siralama(call):
    uid = str(call.from_user.id)
    
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "❌ Yetkin yok!")
        return
    
    data = load_users()
    
    # Puana göre sırala
    kullanicilar = sorted(
        data.items(), 
        key=lambda x: x[1].get("puan", 0), 
        reverse=True
    )[:10]
    
    mesaj = "💰 **En Zengin 10 Kullanıcı:**\n\n"
    
    for i, (k, v) in enumerate(kullanicilar, 1):
        mesaj += f"{i}. @{v.get('username', 'yok')} | {v.get('isim', '')}\n"
        mesaj += f"   💰 {v.get('puan', 0)} puan | 👥 {v.get('referans_sayisi', 0)} ref\n"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Geri", callback_data="admin_geri"))
    
    bot.edit_message_text(
        mesaj,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_satinalmalar")
def admin_satinalmalar(call):
    uid = str(call.from_user.id)
    
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "❌ Yetkin yok!")
        return
    
    data = load_users()
    
    mesaj = "📦 **Son Satın Almalar:**\n\n"
    sayac = 0
    
    for k, v in data.items():
        for urun in v.get("satin_aldiklari", [])[-3:]:  # Son 3 ürün
            if sayac >= 10:
                break
            mesaj += f"👤 @{v.get('username', 'yok')}\n"
            mesaj += f"📦 {urun['urun']} | {urun['fiyat']} puan\n"
            mesaj += f"⏰ {urun['tarih']}\n"
            mesaj += "─" * 20 + "\n"
            sayac += 1
        if sayac >= 10:
            break
    
    if sayac == 0:
        mesaj += "Henüz satın alma yok."
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Geri", callback_data="admin_geri"))
    
    bot.edit_message_text(
        mesaj,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_duyuru")
def admin_duyuru(call):
    uid = str(call.from_user.id)
    
    if uid not in ADMINLER:
        bot.answer_callback_query(call.id, "❌ Yetkin yok!")
        return
    
    bot.edit_message_text(
        "📢 **Duyuru Gönderme**\n\n"
        "Göndermek istediğin duyuru metnini yaz:\n"
        "(İptal için /iptal yaz)",
        call.message.chat.id,
        call.message.message_i
     parse_mode="Markdown"
    )
    
    # Kullanıcıyı duyuru moduna al
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, duyuru_gonder)
    bot.answer_callback_query(call.id)
def duyuru_gonder(message):
    uid = str(message.from_user.id)
    
    if uid not in ADMINLER:
        bot.reply_to(message, "❌ Yetkin yok!")
        return
    
    if message.text == "/iptal":
        bot.reply_to(message, "❌ Duyuru iptal edildi.")
        return
    
    duyuru_metni = message.text
    data = load_users()
    basarili, basarisiz = 0, 0
    
    for user_id in data:
        try:
            bot.send_message(user_id, duyuru_metni)
            basarili += 1
        except:
            basarisiz += 1
            
    bot.send_message(message.chat.id, f"✅ Duyuru Gönderildi!\n📊 Başarılı: {basarili}\n❌ Başarısız: {basarisiz}")

# --- ADMIN GERİ DÖNÜŞ ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_geri")
def admin_geri(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    admin_panel(call.message)

# --- PUAN GÖNDERME FONKSİYONLARI ---
@bot.callback_query_handler(func=lambda call: call.data == "admin_puan_ver")
def admin_puan_ver(call):
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "👤 Puan gönderilecek kullanıcının ID numarasını yazın:")
    bot.register_next_step_handler(msg, puan_id_al)

def puan_id_al(message):
    target_id = message.text
    msg = bot.send_message(message.chat.id, "💰 Gönderilecek puan miktarını rakamla yazın:")
    bot.register_next_step_handler(msg, lambda m: puan_yukle(m, target_id))

def puan_yukle(message, target_id):
    try:
        miktar = int(message.text)
        data = load_users()
        if target_id in data:
            data[target_id]['puan'] = data[target_id].get('puan', 0) + miktar
            save_users(data)
            bot.send_message(message.chat.id, f"✅ {target_id} ID'li kullanıcıya {miktar} puan eklendi!")
            bot.send_message(target_id, f"🎁 Admin tarafından hesabınıza {miktar} puan eklendi!")
        else:
            bot.send_message(message.chat.id, "❌ Kullanıcı veritabanında bulunamadı!")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Hata: Lütfen sadece sayı girin!")

# --- RENDER İÇİN WEB SUNUCUSU (KEEP ALIVE) ---
from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home():
    return "Bot 7/24 Aktif!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOTU BAŞLATAN ANA DÖNGÜ ---
if __name__ == "__main__":
    keep_alive()
    print("Bot aktif başladı...")
    bot.infinity_polling(none_stop=True)

import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Resmi Gazete'den anahtar kelimeleri tarar
def search_resmi_gazete():
    url = "https://www.resmigazete.gov.tr/"
    response = requests.get(url)
    response.encoding = "utf-8"

    keywords = [
        "iş hukuku", "ticaret kanunu", "borçlar kanunu",
        "basın ilan", "resmi ilan ve reklam",
        "radyo ve televizyon", "yayın hizmetleri", "reklam"
    ]
    results = []

    if response.status_code == 200:
        content = response.text
        for keyword in keywords:
            if keyword in content:
                results.append(f"Bulunan: {keyword}")
    else:
        results.append("Resmi Gazete'ye ulaşılamadı.")

    return "\n".join(results)

# Botun komutları
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Merhaba! Resmi Gazete tarayıcısı botu buraya.")

def check(update: Update, context: CallbackContext):
    update.message.reply_text("Resmi Gazete taranıyor...")
    results = search_resmi_gazete()
    update.message.reply_text(results)

# Bot token'ını ayarla
TOKEN = os.getenv("BOT_TOKEN")

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# Komutları tanımla
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("check", check))

# Botu başlat
updater.start_polling()
updater.idle()

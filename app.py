import os
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# פרטי הבוט והטרה-בוקס שלך
BOT_TOKEN = "8147537021:AAG3G4JLiGXGFeo_A9aseWyILAt9SrPMld0"
TERABOX_NDUS = "Ydz8yyYteHui60SoEuxbtttWECL9F953a3AVf9LQ"

def handle_media(update: Update, context: CallbackContext):
    media = update.message.document or update.message.video
    if not media: return
    
    status = update.message.reply_text("📥 Render מוריד את הקובץ...")
    try:
        file = context.bot.get_file(media.file_id)
        file_path = file.download()
        
        status.edit_text("📤 מעלה ל-TeraBox...")
        url = f"https://c-jp.terabox.com/rest/2.0/pcs/file?method=upload&app_id=250528&path=%2F{media.file_id[:5]}.mp4"
        
        with open(file_path, 'rb') as f:
            r = requests.post(url, cookies={"ndus": TERABOX_NDUS}, files={'file': f})
        
        if r.status_code == 200:
            status.edit_text("✅ הצלחנו! הקובץ מחכה לך בטרה-בוקס.")
        else:
            status.edit_text(f"❌ שגיאה בטרה-בוקס: {r.status_code}")
        
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        status.edit_text(f"⚠️ תקלה: {str(e)}")

def main():
    print("🚀 הבוט מתחיל לעבוד...")
    updater = Updater(BOT_TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_media))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# פרטי הבוט והטרה-בוקס שלך
BOT_TOKEN = "8147537021:AAG3G4JLiGXGFeo_A9aseWyILAt9SrPMld0"
TERABOX_NDUS = "Ydz8yyYteHui60SoEuxbtttWECL9F953a3AVf9LQ"

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    media = update.message.document or update.message.video
    if not media: return
    
    status = await update.message.reply_text("📥 Render מוריד את הקובץ...")
    try:
        file = await context.bot.get_file(media.file_id)
        file_path = f"temp_{media.file_id[:5]}.mp4"
        await file.download_to_drive(file_path)
        
        await status.edit_text("📤 מעלה ל-TeraBox...")
        url = f"https://c-jp.terabox.com/rest/2.0/pcs/file?method=upload&app_id=250528&path=%2F{media.file_id[:5]}.mp4"
        
        with open(file_path, 'rb') as f:
            r = requests.post(url, cookies={"ndus": TERABOX_NDUS}, files={'file': f})
        
        if r.status_code == 200:
            await status.edit_text("✅ הצלחנו! הקובץ בטרה-בוקס.")
        else:
            await status.edit_text(f"❌ שגיאה בטרה-בוקס: {r.status_code}")
        
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await status.edit_text(f"⚠️ תקלה: {str(e)}")

def main():
    print("🚀 הבוט מתחיל לעבוד ב-Render...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, handle_media))
    application.run_polling()

if __name__ == '__main__':
    main()

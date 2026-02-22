import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# הגדרת שרת Flask עבור Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    # Render מספק את הפורט במשתנה סביבה, אם לא קיים נשתמש ב-10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# פרטי הבוט שלך (מוודא שאין רווחים בתוך הגרשיים!)
BOT_TOKEN = "8147537021:AAE3WQqs5TltWSh0c4ZGZ8JDtYGgYRUoYUg"
TERABOX_NDUS = "Ydz8yyyteHui60SoEuxbtttWECL9F953a3AVf9LQ"

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and (update.message.document or update.message.video):
        await update.message.reply_text("📥 Render מוריד את הקובץ...")
        # כאן יבוא המשך הלוגיקה שלך

async def main():
    # הפעלת שרת ה-Flask בשרשור נפרד כדי ש-Render יראה פורט פתוח
    Thread(target=run_flask).start()
    
    # הפעלת הבוט
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, handle_media))
    
    print("🚀 הבוט התחיל לעבוד!")
    await application.initialize()
    await application.start_polling()
    # שומר על הבוט רץ
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

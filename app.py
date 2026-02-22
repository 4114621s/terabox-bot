import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# פונקציה להפעלת שרת דמי עבור Render
def run_dummy_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

# פרטי הבוט
BOT_TOKEN = "8147537021:AAE3WQqs5TltWSh0c4ZGZ8JDtYGgYRUoYUg"
TERABOX_NDUS = "Ydz8yyyteHui60SoEuxbtttWECL9F953a3AVf9LQ"

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    media = update.message.document or update.message.video
    if not media: return
    status = await update.message.reply_text("📥 Render מוריד את הקובץ...")
    # כאן יבוא המשך הקוד שלך...
    await status.edit_text("✅ סיימתי!")

def main():
    # הפעלת שרת הדמי בשרשור נפרד
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    # הפעלת הבוט
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, handle_media))
    print("🚀 הבוט מתחיל לעבוד עם שרת דמי...")
    application.run_polling()

if __name__ == "__main__":
    main()

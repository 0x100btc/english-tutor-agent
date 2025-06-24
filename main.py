import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

from handlers.command import start_command, handle_text, handle_voice, set_mode, quiz_kid, handle_quiz_answer
from db import database
#from utils import set_bot_commands

# ==================== 環境設定 ====================
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8080/webhook")
PORT = int(os.getenv("PORT", 8080))

# ==================== 啟動應用 ====================
if __name__ == "__main__":
    print("🚀 啟動 Telegram Webhook 機器人...")
   #db()

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
       # .post_init(set_bot_commands)
        .build()
    )

    app.add_handler(CommandHandler("start_command", start_command))
    app.add_handler(CommandHandler("quiz_kid", quiz_kid))
    app.add_handler(CallbackQueryHandler(handle_quiz_answer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.COMMAND, set_mode))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )
    print("🤖 Bot 啟動中... 使用 Polling 模式")
    app.run_polling()
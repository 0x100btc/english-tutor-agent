# handlers.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telegram.ext import ContextTypes
from services import openai_agent
#from mode import MODE_PROMPTS, get_mode_prompt, mode_state
#from quiz import quiz_data, user_quiz_answers, send_quiz_question
#from voice import process_voice
from gtts import gTTS
import re

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"📥 收到 /start 指令 from {update.effective_user.username}")
    await update.message.reply_text("👋 Hello! English Tutor is ready.")

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = update.message.text.lstrip("/").strip()
    user_id = update.message.from_user.id
    if mode in MODE_PROMPTS:
        mode_state[user_id] = mode
        await update.message.reply_text(f"✅ 模式已切換為 {mode}")
    else:
        await update.message.reply_text("⚠️ 不支援的模式，請用 /tutor_talk /talk /fix /exam /roleplay_cafe")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_text = update.message.text.strip()
        print(f"📩 收到文字訊息：{user_text} from {update.effective_user.username}")
        system_prompt = get_mode_prompt(user_id)
        reply = get_agent_response(system_prompt, user_text)
        print("💬 GPT 回覆：", reply)
        await update.message.reply_text(f"👨‍🏫 教學回覆：\n{reply}")

        english_only = re.sub(r'[^\x00-\x7F]+', '', reply)
        tts = gTTS(text=english_only.strip(), lang='en')
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as audio_file:
            await update.message.reply_voice(voice=audio_file)

    except Exception as e:
        print("❌ 文本錯誤：", e)
        await update.message.reply_text("⚠️ 發生錯誤，請稍後再試")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_voice(update, context)

async def quiz_kid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_quiz_question(update, context)

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    correct = user_quiz_answers.get(user_id)
    selected = query.data
    if selected == correct:
        await query.edit_message_text(f"✅ Correct! The word was '{correct}'.")
        tts = gTTS(text="Great job!", lang='en')
    else:
        await query.edit_message_text(f"❌ Oops! The correct word was '{correct}'.")
        tts = gTTS(text="Try again next time!", lang='en')
    tts.save("result.mp3")
    with open("result.mp3", "rb") as audio_file:
        await context.bot.send_voice(chat_id=query.message.chat_id, voice=audio_file)

async def post_init(application):
    commands = [
        BotCommand("tutor_talk", "翻譯並繼續英文對話"),
        BotCommand("talk", "英文對話模式"),
        BotCommand("fix", "修正英文句子"),
        BotCommand("exam", "英文面試練習"),
        BotCommand("quiz_kid", "兒童單字選擇遊戲")
    ]
    await application.bot.set_my_commands(commands)
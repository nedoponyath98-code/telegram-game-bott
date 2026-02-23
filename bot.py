import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    number = random.randint(1, 100)
    games[user_id] = number
    await update.message.reply_text("🎮 Я загадал число от 1 до 100! Попробуй угадать!")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in games:
        await update.message.reply_text("Напиши /start чтобы начать игру!")
        return

    try:
        user_guess = int(update.message.text)
    except:
        await update.message.reply_text("Введи число!")
        return

    number = games[user_id]

    if user_guess < number:
        await update.message.reply_text("📉 Больше!")
    elif user_guess > number:
        await update.message.reply_text("📈 Меньше!")
    else:
        await update.message.reply_text("🎉 Ты угадал! Напиши /start чтобы сыграть снова!")
        del games[user_id]

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

app.run_polling()

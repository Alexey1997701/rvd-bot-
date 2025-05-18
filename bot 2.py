
import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Токен и ID групп
TOKEN = os.getenv("BOT_TOKEN")
DISPATCH_GROUP_ID = -1002132546465  # ID группы диспетчеров
OPERATOR_GROUP_ID = -1002092021985  # ID группы операторов

logging.basicConfig(level=logging.INFO)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Оставить заявку")],
        [KeyboardButton("Связаться с оператором")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Здравствуйте! Выберите нужное действие:", reply_markup=reply_markup)

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Оставить заявку":
        await update.message.reply_text("Пожалуйста, введите текст вашей заявки.")
        return

    if text == "Связаться с оператором":
        await update.message.reply_text("Напишите сообщение, и оно будет отправлено операторам.")
        context.user_data["mode"] = "operator"
        return

    if context.user_data.get("mode") == "operator":
        context.user_data["mode"] = None
        await context.bot.send_message(chat_id=OPERATOR_GROUP_ID, text=f"Сообщение от клиента:\n\n{text}")
        await update.message.reply_text("Ваше сообщение отправлено операторам.")
    else:
        await context.bot.send_message(chat_id=DISPATCH_GROUP_ID, text=f"Новая заявка:\n\n{text}")
        await update.message.reply_text("Заявка принята. Спасибо!")

# Основной запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

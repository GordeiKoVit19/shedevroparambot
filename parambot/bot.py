from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from secret import BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я помощник для решения 18 задание ЕГЭ с параметром графическим способом."
        "Я умею строить графики. Для ознакомления со всеми функциями напишите /help."
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
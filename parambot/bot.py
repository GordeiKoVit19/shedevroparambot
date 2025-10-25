from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from secret import BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n"
        "Я помощник для решения задач ЕГЭ №18 с параметром графически.\n"
        "Я умею строить графики.\n"
        "Для списка команд нажмите или напишите /help."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Функции программы:\n\n"
        "📈 /graph - строит график и сразу отправляет его пользователю\n"
        "🔄 /restart - запускает функцию /graph и сбрасывает все данные\n\n"
        "💡 Чтобы начать заново, используйте /start"
    )
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()


if __name__ == "__main__":
    main()
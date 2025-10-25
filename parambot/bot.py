from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from secret import BOT_TOKEN

from sympy import sympify, simplify
import re

NUMERATOR, DENOMINATOR = 0, 1
ALLOWED_CHARS = re.compile(r'^[0-9xXa\+\-\*\(\)\sAbs]*$')

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


async def graph_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✏️ Пришлите числитель уравнения.\n"
        "Пример: Abs(3*x) - 2*x - 2 - a**2"
    )
    return NUMERATOR


async def graph_numerator(update, context):
    text = update.message.text.replace("|", "Abs")  # модуль в Abs
    if not ALLOWED_CHARS.match(text):
        await update.message.reply_text(
            "❌ Некорректное выражение. Можно использовать только x, a, числа, +, -, **, (), Abs.\n"
            "Пример: Abs(3*x - 3) - 2*x - 2 - a**2"
        )
        return NUMERATOR
    try:
        expr = sympify(text)
        context.user_data['numerator'] = expr
        await update.message.reply_text(
            "✏️ Отлично! Теперь пришлите знаменатель уравнения.\n"
            "Пример: x**2 - Abs(2*x) - a"
        )
        return DENOMINATOR
    except:
        await update.message.reply_text(
            "❌ Некорректное выражение. Попробуйте ещё раз.\n"
            "Пример: Abs(3*x - 7) - 2*x - 2 - a"
        )
        return NUMERATOR


async def graph_denominator(update, context):
    text = update.message.text.replace("|", "Abs")

    if not ALLOWED_CHARS.match(text):
        await update.message.reply_text(
            "❌ Некорректное выражение. Можно использовать только x, a, числа, +, -, **, (), Abs.\n"
            "Пример: Abs(x**2 - 7) - 2*x - a"
        )
        return DENOMINATOR

    try:
        expr = sympify(text)
        simplified_expr = simplify(expr)
        if simplified_expr.is_Number and simplified_expr == 0:
            await update.message.reply_text(
                "❌ Знаменатель не может быть равен нулю. Попробуйте другое выражение.\n"
                "Пример: Abs(x**2 - 2) - 2*x - a"
            )
            return DENOMINATOR

        context.user_data['denominator'] = expr
        await update.message.reply_text(
            f"✅ Получено!\nЧислитель: {context.user_data['numerator']}\n"
            f"Знаменатель: {context.user_data['denominator']}\n"
            "Теперь можно строить график a(x)."
        )
        return ConversationHandler.END
    except:
        await update.message.reply_text(
            "❌ Некорректное выражение. Попробуйте ещё раз.\n"
            "Пример: Abs(x**2 - 3) - 2*x - a"
        )
        return DENOMINATOR


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🔄 Бот перезапущен. Можно начать заново!")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('graph', graph_start)],
        states={
            NUMERATOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, graph_numerator)],
            DENOMINATOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, graph_denominator)],
        },
        fallbacks=[CommandHandler('restart', restart)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("restart", restart))

    app.run_polling()


if __name__ == "__main__":
    main()
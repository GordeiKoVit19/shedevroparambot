from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from secret import BOT_TOKEN
from solver.solve_fraction import solve_numerator, check_denominator
from graphing.plot import plot_graph
from sympy import sympify, simplify
import re

NUMERATOR, DENOMINATOR = 0, 1
ALLOWED_CHARS = re.compile(r'^[0-9xXa\+\-\*/\(\)\s\^Abs]*$')

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


# --- graph_numerator ---
async def graph_numerator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not ALLOWED_CHARS.match(text):
        await update.message.reply_text(
            "❌ Некорректное выражение. Разрешено использовать только x, a, числа, +, -, *, /, ^, (), Abs.\n"
            "Пример: Abs(3*x - 3) - 2*x - 2 - a^2"
        )
        return NUMERATOR

    try:
        # sympify с convert_xor=True чтобы ^ воспринималась как степень
        expr = sympify(text, convert_xor=True)
        context.user_data['numerator'] = expr

        await update.message.reply_text(
            "✏️ Отлично! Теперь пришлите знаменатель уравнения.\n"
            "Пример: x^2 - Abs(2*x) - a"
        )
        return DENOMINATOR

    except:
        await update.message.reply_text(
            "❌ Некорректное выражение. Попробуйте ещё раз."
        )
        return NUMERATOR




# --- graph_denominator ---
async def graph_denominator(update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not ALLOWED_CHARS.match(text):
        await update.message.reply_text(
            "❌ Некорректное выражение. Разрешено использовать только x, a, числа, +, -, *, /, ^, (), Abs.\n"
            "Пример: x^2 - Abs(2*x) - a"
        )
        return DENOMINATOR

    try:
        expr = sympify(text, convert_xor=True)
        simplified_expr = simplify(expr)
        if simplified_expr.is_Number and simplified_expr == 0:
            await update.message.reply_text(
                "❌ Знаменатель не может быть равен нулю. Попробуйте другое выражение."
            )
            return DENOMINATOR

        context.user_data['denominator'] = expr

        filename = plot_graph(
            context.user_data['numerator'],
            context.user_data['denominator'],
            limit=10,
            y_limit=10
        )
        await update.message.reply_photo(photo=open(filename, 'rb'))

    except Exception as e:
        print("Ошибка построения графика:", e)
        await update.message.reply_text(
            "❌ Некорректное выражение или ошибка при построении графика. Попробуйте ещё раз."
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
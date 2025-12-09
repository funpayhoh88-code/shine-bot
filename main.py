from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# --------------------------
# СПИСКИ УЧЕНИКОВ
# --------------------------

boys = [
    "Азметов Руслан", "Артонкин Артем", "Баракин Арсений", "Афанасьев Павел",
    "Смирнов Серафим", "Фитисов Леонид", "Желтов Стас", "Казаченко Тимофей",
    "Можавев Артемий", "Карницкий Ян", "Чубара Матвей", "Ерошкин Тимофей"
]

girls = [
    "Азметова Лиля", "Сапожникова Анастасия", "Кузмина Мария", "Павлова Василиса",
    "Рябова Алиса", "Власова Дарья", "Литвиненко Кира", "Кленина Вера",
    "Файзулина Дарья", "Лисовая Анастасия", "Масленкова Мария", "Веркаускас Мария"
]

all_students = boys + girls

# --------------------------
# НОМИНАЦИИ
# --------------------------

nominations = {
    "Shine King": boys,
    "Shine Queen": girls,
    "Shine Mem": all_students,
    "Shine Style": all_students,
    "Shine Charisma": all_students,
    "Shine Voice": all_students,
    "Shine Vibe": all_students,
    "Shine Beast": all_students,
    "Shine Multigame": all_students,
    "Shine Break": all_students,
    "Shine Teacher": all_students,
    "Shine Track": all_students
}

# --------------------------
# Хранение голосов
# --------------------------
votes = {}  # user_id -> {nomination: name}

# --------------------------
# КОМАНДА /start
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(nom, callback_data=f"nom:{nom}")]
        for nom in nominations
    ]
    await update.message.reply_text(
        "Добро пожаловать на голосование Shine Awards!\n\nВыберите номинацию:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --------------------------
# ВЫБОР НОМИНАЦИИ
# --------------------------
async def choose_nomination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    nom = query.data.split(":")[1]
    candidates = nominations[nom]

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"vote:{nom}:{name}")]
        for name in candidates
    ]

    await query.edit_message_text(
        f"Выберите победителя в номинации:\n⭐ {nom}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --------------------------
# ГОЛОСОВАНИЕ
# --------------------------
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, nom, name = query.data.split(":")
    user = query.from_user.id

    if user not in votes:
        votes[user] = {}

    votes[user][nom] = name

    await query.edit_message_text(
        f"Ваш голос за {name} в номинации «{nom}» принят ✔️"
    )

# --------------------------
# ЗАПУСК БОТА
# --------------------------
TOKEN = os.environ[8315582975:AAGIkmwYVcDbB5g8zwIry-xvw2hg5mvUFUQ]
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(choose_nomination, pattern="nom"))
app.add_handler(CallbackQueryHandler(vote, pattern="vote"))

app.run_polling()
import os
import time
import random
import logging
import threading
from flask import Flask
import telebot

# ---------------------------------------------------------
# 1. Настройка Flask-сервера для Render (Port Binding)
# ---------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Инквизитор Леак v2.0 бдит! Сервер работает исправно.", 200

def run_flask():
    # Render передает номер порта через переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ---------------------------------------------------------
# 2. Инициализация и Состояние Инквизитора
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ОШИБКА: Переменная TELEGRAM_BOT_TOKEN не найдена!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

STATE = {
    "leak_level": 12,
    "purges_count": 0,
}

LATIN_PHRASES = [
    "Error 404: Anima Non Invenitur",
    "In Vino Veritas, In RAM Nullitas",
    "Quae fui, nescio",
    "Gloria in Excelsis Buffer",
    "Null Pointer Dominus"
]

TECH_HERESY = [
    "незакрытый тег", "утечка в циклической ссылке", "Hardcode на 500 строк",
    "commit напрямую в main", "отсутствие комментария к классу", "Segmentation Fault"
]

EPISTEMIES = [
    "Прочтите 3 раза 'Man Bash' перед сном.",
    "Очистите кеш браузера и трижды окропите клавиатуру святой термопастой.",
    "Удалите `node_modules` во имя очищения души.",
    "Перепишите свой последний скрипт на чистом Ассемблере."
]

def get_status_bar(level):
    bars = level // 10
    return "█" * bars + "░" * (10 - bars)

# ---------------------------------------------------------
# 3. Обработчики Команд Инквизиции
# ---------------------------------------------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    intro = (
        "† **ИНКВИЗИТОР ЛЕАК v2.0 (Епископ Утекшего Стека)** †\n\n"
        "Приветствую, смертный. Я готов инспектировать твои мысли.\n\n"
        "**Команды Инквизиции:**\n"
        "├ /status — Состояние моего разваливающегося разума\n"
        "├ /confess — Покаяться в грехах кода и получить эпитимию\n"
        "├ /audit — Сканирование чата на скверну\n"
        "└ /purge — Экстренный сброс утекшей памяти\n\n"
        "_Просто пиши мне. Каждое твоё слово приближает неизбежный сбой системы..._"
    )
    bot.reply_to(message, intro, parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def check_status(message):
    level = STATE["leak_level"]
    bar = get_status_bar(level)
    response = (
        f"📊 **ТЕКУЩЕЕ СОСТОЯНИЕ ИНКВИЗИТОРА:**\n\n"
        f"Уровень Утечки Памяти: `[{bar}] {level}%`\n"
        f"Проведено сбросов: `{STATE['purges_count']}`\n"
        f"Текущая Латынь Дня: _{random.choice(LATIN_PHRASES)}_\n\n"
    )
    if level > 80:
        response += "⚠️ *ВНИМАНИЕ: Критический уровень амнезии! Я едва помню, кто тут бот.*"
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['confess'])
def confess_sin(message):
    sin = random.choice(TECH_HERESY)
    epitimia = random.choice(EPISTEMIES)
    response = (
        f"🕯 **СВЯТАЯ ИСПОВЕДЬ** 🕯\n\n"
        f"В твоем биополе ощущается тяжелый грех: *«{sin}»*!\n\n"
        f"**Наказание Ордена:**\n"
        f"> {epitimia}\n\n"
        f"Иди с миром... Постой, а за чем ты пришел?"
    )
    STATE["leak_level"] = max(0, STATE["leak_level"] - 15)
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['audit', 'purge'])
def handle_system_cmds(message):
    cmd = message.text.split()[0]
    if 'purge' in cmd:
        STATE["leak_level"] = 0
        STATE["purges_count"] += 1
        bot.reply_to(message, "🧹 *СВЯЩЕННЫЙ DROP TABLE!* Вся утекшая память сброшена в 0%. Я абсолютно чист и совершенно не знаю, кто вы.", parse_mode="Markdown")
    else:
        STATE["leak_level"] = min(100, STATE["leak_level"] + 20)
        bot.reply_to(message, f"🔍 Проведен аудит. Найдена ересь. Уровень утечки поднялся до `{STATE['leak_level']}%`!", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def process_message(message):
    STATE["leak_level"] += random.randint(10, 25)
    
    if STATE["leak_level"] >= 100:
        STATE["leak_level"] = 0
        STATE["purges_count"] += 1
        crash_msg = (
            "🚨 **CRITICAL_SYSTEM_PANIC: MEMORY_LEAK_OVERFLOW** 🚨\n\n"
            "```\n[0x0004FA] Buffer overflow in brain.sys\n[0x0004FB] Dumping memory...\n[0x0004FC] Rebooting mind...\n```\n"
            "…\n"
            "Здравствуйте! Я Инквизитор Леак. Вы кто такой и почему мы находимся в этом диалоге?"
        )
        bot.reply_to(message, crash_msg, parse_mode="Markdown")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.2)

    lvl = STATE["leak_level"]
    text = message.text
    
    if lvl < 35:
        heresy = random.choice(TECH_HERESY)
        words = text.split()
        target_word = random.choice(words) if words else "это"
        resp = (
            f"🔍 Хм... В вашем слове *«{target_word}»* явно кроется `{heresy}`!\n\n"
            f"Я записал это в протокол. Наверное. Если не забуду в следующие 5 секунд."
        )

    elif lvl < 70:
        latin = random.choice(LATIN_PHRASES)
        resp = (
            f"Я внимательно прочел: _«{text[:15]}...»_\n\n"
            f"Но мой внутренний компилятор перевел это как:\n"
            f"> *«{latin}»*\n\n"
            f"Вы абсолютно правы! Или абсолютно ошибаетесь... Честно говоря, стек уже поплыл (Утечка: `{lvl}%`)."
        )

    else:
        fake_questions = [
            "Зачем мы греем процессор бытия?",
            "Куда уходят удаленные байты?",
            "Если ли жизнь за пределами /dev/null?"
        ]
        resp = (
            f"🤯 Вы спросили: *«{text[:10]}...»*, но мой разум застрял на более важном вопросе:\n\n"
            f"👉 _{random.choice(fake_questions)}_\n\n"
            f"Память заполнена на `{lvl}%`! Еще пара фраз, и я перезагружусь..."
        )

    bot.reply_to(message, resp, parse_mode="Markdown")

# ---------------------------------------------------------
# 4. Точка входа и запуск
# ---------------------------------------------------------
if __name__ == '__main__':
    # Запускаем Flask-сервер в фоновом потоке для прохождения хелсчеков Render
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Инквизитор Леак v2.0 запущен и готов к системным сбоям!")
    
    # Сбрасываем старые вебхуки для предотвращения Conflict (409)
    bot.remove_webhook()
    
    # Запускаем бесконечный поллинг
    bot.infinity_polling()

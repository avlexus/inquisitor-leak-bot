import os
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
    return "Инквизитор Леак бдит! Сервер работает исправно.", 200

def run_flask():
    # Render передает номер порта через переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    # Запускаем Flask на всех интерфейсах 0.0.0.0
    app.run(host='0.0.0.0', port=port)

# ---------------------------------------------------------
# 2. Инициализация Telegram-бота
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("ОШИБКА: Токен TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Список случайных утечек памяти
LEAK_RESPONSES = [
    "🚨 ВНИМАНИЕ: Зафиксирована утечка священной памяти в секторе 0x7FFF8! Паника ядра!",
    "⚠️ Обнаружен неконтролируемый утекающий поток! Память уходит в Бездну...",
    "💾 Инквизитор Леак извлек 512 МБ из вашей душевной сущности!",
    "💥 Ошибка сегментации (Segmentation fault)! Священный стек переполнен!",
    "🛡️ Логи сбоя отправлены в Орден. Память очищена... но какой ценой?"
]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Приветствую, Брат по Ордену! ⚔️\n\n"
        "Я — **Инквизитор Леак v2.0**, страж системных сбоев и хранитель памяти!\n"
        "Напиши мне любое сообщение или команду /leak, чтобы активировать проверку."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['leak'])
def trigger_leak(message):
    response = random.choice(LEAK_RESPONSES)
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(
        message, 
        f"Инквизиция получила твое послание: «{message.text}».\n"
        f"Система стабильна, утечек не обнаружено."
    )

# ---------------------------------------------------------
# 3. Точка входа и запуск
# ---------------------------------------------------------
if __name__ == '__main__':
    # Запускаем Flask в отдельном фоновом потоке
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Инквизитор Леак v2.0 запущен и готов к системным сбоям!")
    
    # Сбрасываем старые вебхуки, чтобы избежать ошибки 409 Conflict
    bot.remove_webhook()
    
    # Запускаем бесконечный поллинг
    bot.infinity_polling()

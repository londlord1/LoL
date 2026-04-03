import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

# === ЗАМЕНИ НА СВОИ ТОКЕНЫ ===
TELEGRAM_TOKEN = "8678845826:AAFNS_Qf_MzTCkSbw28oOGGtBVQTgdpFJB4"
DEEPSEEK_API_KEY = "sk-f0bc6efb38d04a18aabeae28fe50036f"

async def start(update, context):
    await update.message.reply_text("Привет! Я бот-карьерист. Напиши /help")

async def help_command(update, context):
    await update.message.reply_text("/start - начать\n/help - помощь\n/vacancies [запрос] - найти вакансии")

async def vacancies(update, context):
    query = " ".join(context.args) if context.args else "стажёр"
    url = "https://api.hh.ru/vacancies"
    params = {"text": query, "experience": "noExperience", "per_page": 3}
    headers = {"User-Agent": "CareerBot/1.0"}
    
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code != 200:
        await update.message.reply_text("Ошибка поиска вакансий")
        return
    
    items = resp.json().get("items", [])
    if not items:
        await update.message.reply_text("Вакансий не найдено")
        return
    
    for v in items:
        text = f"{v['name']}\n{v['employer']['name']}\n{v['alternate_url']}"
        await update.message.reply_text(text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("vacancies", vacancies))
    
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()

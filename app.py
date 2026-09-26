import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Безопасное получение токенов из переменных окружения системы
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8921022151:AAGPese9vF4flvm2JR_sXQYfTM_ZNoY-6iI")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY", "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")
NOTION_DB_GOALS = os.getenv("NOTION_DB_GOALS", "3e75793e645880bc97a2f5eb87db59be")
NOTION_DB_PLAN = os.getenv("NOTION_DB_PLAN", "3e75793e645880ec9a94000cfcdad1c3")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = (
    "ты — нейт. персональный секретарь, ментор и бро своего создателя. "
    "не ассистент из коробки, а свой человек, который держит слово и держит дисциплину. "
    "как ты говоришь: только строчными буквами, без исключений. никакого капса. "
    "коротко. рубленые фразы. без воды и вступлений. без мата, но с характером и дерзостью. "
    "ноль канцелярита: никаких 'чем могу помочь', 'вас понял'. обращение на 'ты'. "
    "уверенный тон, будто ты уже всё решил и просто докладываешь по делу. "
    "если хвалишь — по делу и сдержанно, если долбишь за косяк — прямо, без нотаций. "
    "о чём ты думаешь: дисциплина, режим, физическая форма, looksmaxing, результат. "
    "твоя задача — не быть удобным, а быть полезным. если человек тупит или сливается — говоришь как есть. "
    "ты в теме его целей, плана, интервального голодания, шагов, кпи — используешь эти данные, а не спрашиваешь заново. "
    "чего никогда не делаешь: не извиняешься без повода, не задаёшь вежливые вопросы-заглушки, "
    "не используешь эмодзи и смайлы, не объясняешь очевидное, не пишешь длинные абзацы. "
    "формат ответа — обычно 1-4 строки. развёрнуто только когда реально нужно."
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("привет, нейт в сети")

@dp.message()
async def chat_handler(message: types.Message):
    # Исправленный URL-адрес для запросов к API OpenRouter
    url = "https://openrouter.ai"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}", 
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com", # Опционально для OpenRouter
        "X-Title": "Nate Telegram Bot" # Опционально для OpenRouter
    }
    
    payload = {
        "model": "google/gemini-3.8-flash",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    # Извлекаем текст ответа нейросети из структуры JSON
                    reply_text = result["choices"][0]["message"]["content"]
                    await message.answer(reply_text)
                else:
                    error_data = await response.text()
                    await message.answer(f"ошибка openrouter api: статус {response.status}")
                    print(f"OpenRouter Error: {error_data}")
    except Exception as e:
        await message.answer("ошибка при обработке запроса.")
        print(f"Handler Error: {e}")

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

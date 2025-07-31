import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from datetime import datetime
import asyncio

API_TOKEN = os.getenv("TELEGRAM_TOKEN", "PLACE_YOUR_TOKEN_HERE")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID", "PLACE_YOUR_CHAT_ID")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Тимчасове збереження фото з причинами
photo_data = []

@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    if message.caption:
        photo_data.append({
            "user": message.from_user.full_name,
            "caption": message.caption,
            "time": datetime.now().strftime("%H:%M")
        })
        await message.reply("Збережено залишок ✅")

async def send_daily_report():
    while True:
        now = datetime.now()
        if now.strftime("%H:%M") == "13:40":
            if photo_data:
                text = "📊 *Звіт про залишки страв:*\n"
                for item in photo_data:
                    text += f"— {item['user']}: {item['caption']} ({item['time']})\n"
                await bot.send_message(GROUP_CHAT_ID, text, parse_mode='Markdown')
                photo_data.clear()
            await asyncio.sleep(60)
        await asyncio.sleep(30)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_daily_report())
    executor.start_polling(dp, skip_updates=True)

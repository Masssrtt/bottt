import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

API_TOKEN = "7669768570:AAGoEM5v22-UXc9LdcVHpxX57V6qRIu5K6o"
ADMIN_IDS = {1483826275, 5796861712}  # Оновлений список адміністраторів

# Налаштування логування
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Файл для збереження балансу
BALANCE_FILE = "balances.json"

def load_balances():
    try:
        with open(BALANCE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_balances(balances):
    with open(BALANCE_FILE, "w") as f:
        json.dump(balances, f, indent=4)

balances = load_balances()

@dp.message(Command("profile"))
async def profile(message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or "Без ніка"
    balance = balances.get(user_id, 0)
    await message.reply(f"👤 Профіль: @{username}\n💰 Баланс: {balance} балів")

@dp.message(Command("uspr"))
async def uspr(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if not message.reply_to_message or message.reply_to_message.from_user.is_bot:
        await message.reply("❌ Цю команду потрібно використовувати у відповідь на повідомлення користувача.")
        return
    user_id = str(message.reply_to_message.from_user.id)
    username = message.reply_to_message.from_user.username or "Без ніка"
    balance = balances.get(user_id, 0)
    await message.reply(f"👤 @{username}\n💰 Баланс: {balance} балів")

@dp.message(Command("plmi"))
async def plmi(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if not message.reply_to_message or message.reply_to_message.from_user.is_bot:
        await message.reply("❌ Цю команду потрібно використовувати у відповідь на повідомлення користувача.")
        return
    try:
        amount = int(message.text.split()[1].replace("+", ""))  # Видаляємо '+' для коректного парсингу
    except (IndexError, ValueError):
        await message.reply("❌ Вкажіть число для зміни балансу (наприклад: /plmi +10 або /plmi -5)")
        return
    user_id = str(message.reply_to_message.from_user.id)
    balances[user_id] = balances.get(user_id, 0) + amount
    save_balances(balances)
    await message.reply(f"✅ Баланс оновлено! Новий баланс: {balances[user_id]} балів")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

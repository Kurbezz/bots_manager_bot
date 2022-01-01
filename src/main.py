import os
import re
from typing import Optional

from aiogram import Bot, Dispatcher, executor, types
import httpx


BOT_TOKEN = os.environ["BOT_TOKEN"]
MANAGER_URL = os.environ["MANAGER_URL"]
MANAGER_API_KEY = os.environ["MANAGER_API_KEY"]

token_regexp = re.compile(r"[0-9]+:[0-9a-zA-Z-]+")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def get_token(text: str) -> Optional[str]:
    match = token_regexp.findall(text)

    if match:
        return match[0]

    return None


async def _make_register_request(user_id: int, token: str) -> bool:
    async with httpx.AsyncClient() as client:
        data = {"token": token, "user": user_id, "status": "pending"}
        response = await client.post(
            MANAGER_URL, json=data, headers={"Authorization": MANAGER_API_KEY}
        )
        return response.status_code == 200


@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    await message.reply(
        """
Зарегиструй бота в @BotFather .
И перешли сюда сообщение об успешной регистрации.
(Начинается с: Done! Congratulations on your new bot.)
    """
    )


@dp.message_handler()
async def register(message: types.Message):
    if not message.text:
        return await message.reply("Присылай сюда текст!")

    token = get_token(message.text)

    if token is None:
        return await message.reply("Ошибка 2!")

    test_bot = Bot(token=token)

    try:
        me = await test_bot.get_me()
        registered = await _make_register_request(message.from_user.id, token)

        if registered:
            await message.reply(f"@{me.username} зарегистрирован!")
        else:
            await message.reply("Ошибка! Возможно бот уже зарегистрирован!")
    except Exception:
        await message.reply("Ошибка! Что-то не так с ботом!")
    finally:
        await bot.close()


if __name__ == "__main__":
    executor.start_polling(dp)

import asyncio

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager

me_router = Router()


@me_router.message(F.chat.type == ChatType.PRIVATE, Command("me"), StateFilter(None))
async def me(message: Message, dialog_manager: DialogManager, **data):
    m = await message.answer(f"Your id: {message.from_user.id}")
    await asyncio.sleep(45)
    await m.delete()

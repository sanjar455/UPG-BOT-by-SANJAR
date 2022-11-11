import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.menu import main_menu
from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(tg_id=message.from_user.id,
                    full_name=name, username=message.from_user.username)
        await message.answer(f"Xush kelibsiz! {name}\n\nBizning online do'konimizdan kerakli bo'lgan mahsulotlarni topishingiz mumkin.", reply_markup=main_menu)
        # Adminga xabar beramiz
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
        await message.answer(f"Xush kelibsiz! {name}\n\nBizning online do'konimizdan kerakli bo'lgan mahsulotlarni topishingiz mumkin.", reply_markup=main_menu)

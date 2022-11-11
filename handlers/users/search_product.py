from loader import dp, db
from aiogram import types
from states.main import ShopState
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="search")
async def get_search_products(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("🔎 Nima qidirmoqchisiz?\n\nMahsulot haqida ma'lumot jo'nating")
    await ShopState.search.set()


@dp.message_handler(state=ShopState.search)
async def get_search_text(message: types.Message, state: FSMContext):
    results = db.search_products(query=message.text)
    
    if results:
        await message.answer(f"{message.text} topilgan ma'lumotlar ...")
        for product in results:
            if product[-2] is not None:
                await message.answer_photo(photo=product[-3], caption=f"<b>{product[1]}</b>\n<u>Price: {product[-4]}</u>\n\n<i>{product[3]}</i>")
            else:
                await message.answer(text=f"<b>{product[1]}</b>\n<u>Price: {product[-4]}</u>\n\n<i>{product[3]}</i>")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton(text="Qayta izlash 🔄", callback_data="search"))
        await message.answer("Bunday ma'lumot topilmadi 😭", reply_markup=markup)
    await state.finish()
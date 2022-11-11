from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, dp
from aiogram import types
from keyboards.inline.menu import back, home
from states.main import ShopState
from aiogram.dispatcher import FSMContext

@dp.callback_query_handler(state=ShopState.sub_category)
async def get_all_data(call: types.CallbackQuery, state: FSMContext):
    sub_cat_info = db.get_sub_category_info(slug=call.data)
    sub_cat_id = sub_cat_info[0]
    sub_cat_title = sub_cat_info[1]
    sub_cat_image = sub_cat_info[3]
    await state.update_data({
        'sub_cat_id': sub_cat_id,
        'sub_cat_slug': call.data
    })
    products = db.select_all_products_by_sub_cat_id(subcategory_id=sub_cat_id)
    markup = InlineKeyboardMarkup(row_width=2)
    for product in products:
        markup.insert(InlineKeyboardButton(text=product[0], callback_data=product[1]))
    markup.add(back, home)
    if sub_cat_image is not None:
        await call.message.delete()
        await call.message.answer_photo(photo=sub_cat_image, caption=f"{sub_cat_title} kategoriyasidagi barcha mahsulotlar ro'yhati", reply_markup=markup)
    else:
        await call.message.edit_text(f"{sub_cat_title} kategoriyasidagi barcha kichik kategoriyalar ro'yhati", reply_markup=markup)
    await ShopState.next()
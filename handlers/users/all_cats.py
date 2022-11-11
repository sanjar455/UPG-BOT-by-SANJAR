from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db, dp
from aiogram import types
from keyboards.inline.menu import back, home
from states.main import ShopState
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import get_all_cats


@dp.callback_query_handler(text="cats")
async def all_categories(call: types.CallbackQuery):
    cats_info = db.select_all_cats()
    await call.message.edit_text("Barcha kategoriyalar ro'yhati", reply_markup=get_all_cats(cats_info))
    await ShopState.category.set()


@dp.callback_query_handler(state=ShopState.category)
async def get_sub_categories(call: types.CallbackQuery, state: FSMContext):
    slug = call.data
    cat_info = db.get_category_info(slug=slug)
    cat_id = cat_info[0]
    cat_title = cat_info[1]
    cat_image = cat_info[3]
    await state.update_data({
        "cat_id": cat_id,
        "cat_slug": slug
    })
    sub_cats = db.select_all_sub_cats_by_cat_id(category_id=cat_id)
    markup = InlineKeyboardMarkup(row_width=2)
    for sub_cat in sub_cats:
        markup.insert(InlineKeyboardButton(text=sub_cat[0], callback_data=sub_cat[1]))
    markup.add(back, home)
    if cat_image is not None:
        await call.message.delete()
        await call.message.answer_photo(photo=cat_image, caption=f"{cat_title} kategoriyasidagi barcha kichik kategoriyalar ro'yhati", reply_markup=markup)
    else:
        await call.message.edit_text(f"{cat_title} kategoriyasidagi barcha kichik kategoriyalar ro'yhati", reply_markup=markup)
    await ShopState.next()

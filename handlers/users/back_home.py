from loader import dp, db
from aiogram import types
from states.main import ShopState
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import main_menu, get_all_cats, back, home
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.callback_query_handler(text="home", state="*")
async def back_to_home(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer(f"Bizning online do'konimizdan kerakli bo'lgan mahsulotlarni topishingiz mumkin.", reply_markup=main_menu)

@dp.callback_query_handler(text="back", state=ShopState.category)
async def back_to_home(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Bizning online do'konimizdan kerakli bo'lgan mahsulotlarni topishingiz mumkin.", reply_markup=main_menu)
    await state.finish()

@dp.callback_query_handler(text="back", state=ShopState.sub_category)
async def back_to_cats(call: types.CallbackQuery, state: FSMContext):
    cats_info = db.select_all_cats()
    await call.message.delete()
    await call.message.answer("Barcha kategoriyalar ro'yhati", reply_markup=get_all_cats(cats_info))
    await ShopState.category.set()

@dp.callback_query_handler(text="back", state=ShopState.product)
async def back_to_cats(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat_id = data.get('cat_id')
    cat_slug = data.get('cat_slug')

    cat_info = db.get_category_info(slug=cat_slug)
    cat_id = cat_info[0]
    cat_title = cat_info[1]
    cat_image = cat_info[3]
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
    await ShopState.sub_category.set()


@dp.callback_query_handler(text="back", state=ShopState.amount)
async def back_to_sub_cats(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sub_cat_id = data.get('sub_cat_id')
    sub_cat_slug = data.get('sub_cat_slug')

    sub_cat_info = db.get_sub_category_info(slug=sub_cat_slug)
    sub_cat_id = sub_cat_info[0]
    sub_cat_title = sub_cat_info[1]
    sub_cat_image = sub_cat_info[3]
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
    await ShopState.product.set()
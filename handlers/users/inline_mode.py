from loader import dp, db
from aiogram import types
from keyboards.inline.menu import main_menu


@dp.inline_handler(text="category")
async def get_all_cats(query: types.InlineQuery):
    cats = db.select_all_cats()
    cats_query = []
    for cat in cats:
        sub_cats = db.select_all_sub_cats_by_cat_id(category_id=cat[0])
        markup = types.InlineKeyboardMarkup(row_width=2)
        for sub_cat in sub_cats:
            markup.insert(types.InlineKeyboardButton(text=sub_cat[0], callback_data=sub_cat[1]))
        cats_query.append(
            types.InlineQueryResultArticle(
                id=cat[0],
                title=cat[1],
                description=cat[-1],
                input_message_content=types.InputMessageContent(message_text=f"All {cat[1]}s"),
                reply_markup=markup
            )
        )
    await query.answer(cats_query)


@dp.inline_handler()
async def get_query(query: types.InlineQuery):
    results = db.search_products(query.query)
    print(results)
    products = []
    for product in results:
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton(text="Batafsil ma'lumot", url=product[-2]))
        products.append(
            types.InlineQueryResultPhoto(
                id=product[0],
                photo_url = product[-3],
                thumb_url = product[-3],
                title=product[1],
                caption=f"<b>{product[1]}</b>\n<u>Price: {product[-4]}</u>\n\n<i>{product[3]}</i>",
                parse_mode="html",
                reply_markup=markup
            )
        )
    await query.answer(products)
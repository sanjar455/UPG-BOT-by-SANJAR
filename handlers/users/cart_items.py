from loader import dp, db, bot
from aiogram import types
from states.main import ShopState
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import get_cart_items, main_menu
from utils.misc.product import Product
from aiogram.types import LabeledPrice
from data.shippings import *
from data.config import ADMINS


@dp.callback_query_handler(text="cart")
async def get_items(call: types.CallbackQuery, state: FSMContext):
    items = db.get_cart_items(tg_id=call.from_user.id)
    
    if items:
        products_info = []
        msg = ""
        total = 0
        for item in items:
            product = db.get_product_info(id=item[-2])
            amount = item[-1]
            price = product[-4]
            title = product[1]
            total_price = price * amount
            total += total_price
            print(total_price)
            msg += f"<b>{title} x {amount} = {total_price}</b>\n"
            products_info.append((product[0], title))
        msg += f"\n<i>Umumiy to'lov miqdori:</i> <b>{total}</b>"
        await call.message.edit_text(msg, reply_markup=get_cart_items(items=products_info))
        await ShopState.cart.set()
    else:
        await call.answer("Sizning savatingiz hozircha bo'sh", show_alert=True)


@dp.callback_query_handler(text="clear", state=ShopState.cart)
async def clear_cart(call: types.CallbackQuery, state: FSMContext):
    db.delete_product_cart(tg_id=call.from_user.id)
    await call.answer("Savatingiz bo'shatildi", show_alert=True)
    await call.message.edit_text("Bizning online do'konimizdan kerakli bo'lgan mahsulotlarni topishingiz mumkin.", reply_markup=main_menu)
    await state.finish()

@dp.callback_query_handler(text="order", state=ShopState.cart)
async def save_order(call: types.CallbackQuery, state: FSMContext):
    items = db.get_cart_items(tg_id=call.from_user.id)
    labeled_prices = []
    msg = ""
    for item in items:
        product = db.get_product_info(id=item[-2])
        amount = item[-1]
        price = product[-4]
        title = product[1]
        total_price = price * amount
        msg += f"{title} x {amount} = {total_price}\n"
        labeled_prices.append(LabeledPrice(label=title, amount=int(total_price * 100)))

    products = Product(
        title="To'lov qilish uchun quyidagi tugmani bosing.",
        description=msg,
        currency="UZS",
        prices=labeled_prices,
        start_parameter="create_invoice_macbook",
        photo_url='https://visme.co/blog/wp-content/uploads/2021/08/How-to-make-an-invoice-Header.jpg',
        photo_width=1280,
        photo_height=350,
        # photo_size=600,
        need_email=True,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
        is_flexible=True
    )
    await bot.send_invoice(chat_id=call.from_user.id,
                           **products.generate_invoice(),
                           payload="payload:macbook")


@dp.shipping_query_handler(state=ShopState.cart)
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "urganch":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)

@dp.pre_checkout_query_handler(state=ShopState.cart)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!")
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")
    db.delete_product_cart(tg_id=pre_checkout_query.from_user.id)


@dp.callback_query_handler(state=ShopState.cart)
async def delete_cart_product(call: types.CallbackQuery, state):
    product_id = int(call.data)
    db.delete_product_cart(tg_id=call.from_user.id, product_id=product_id)
    items = db.get_cart_items(tg_id=call.from_user.id)

    if items:
        products_info = []
        msg = ""
        total = 0
        for item in items:
            product = db.get_product_info(id=item[-2])
            amount = item[-1]
            price = product[-4]
            title = product[1]
            total_price = price * amount
            total += total_price
            msg += f"<b>{title} x {amount} = {total_price}</b>\n"
            products_info.append((product[0], title))
        msg += f"\n<i>Umumiy to'lov miqdori:</i> <b>{total}</b>"
        await call.message.edit_text(msg, reply_markup=get_cart_items(items=products_info))
    else:
        await call.answer("Savatingiz bo'shatildi", show_alert=True)
        await call.message.edit_text("Bizning online do'konimizdan kerakli bo'lgan mahsulotlarni topishingiz mumkin.", reply_markup=main_menu)
        await state.finish()

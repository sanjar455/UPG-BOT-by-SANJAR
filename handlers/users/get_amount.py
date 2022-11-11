from loader import dp, db
from aiogram import types
from states.main import ShopState
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import main_menu


@dp.callback_query_handler(state=ShopState.amount)
async def get_product_amount(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = data.get('product_id')
    await call.message.delete()
    call_data = call.data

    if call_data.isdigit():
        amount = int(call_data)
        db.add_product(tg_id=call.from_user.id, product_id=product_id, amount=amount)
    elif call_data == "like":
        pass
    
    await call.message.answer("Mahsulot savatchaga qo'shildi", reply_markup=main_menu)
    await state.finish()
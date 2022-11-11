from aiogram.dispatcher.filters.state import StatesGroup, State


class ShopState(StatesGroup):
    category = State()
    sub_category = State()
    product = State()
    amount = State()
    cart = State()
    search = State()
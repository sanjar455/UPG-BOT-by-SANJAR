from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.sqlite import Database
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
<<<<<<< HEAD
db = Database(path_to_db="D:/sanjar/data/UPGBot/data/main.db")
=======
db = Database(path_to_db="D:/BOT/UPGBot/data/main.db")
>>>>>>> ae1d5241c341c01fd52cccf98bc1e286901da43b

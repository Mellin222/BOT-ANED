from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bs4 import BeautifulSoup
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests

bot = Bot(token='5868006910:AAFHmDDKH9Qayv9dg2IyfEr3K1ZTVgdEZ2E')
dp = Dispatcher(bot)

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Анекдот'))



async def get_joke():
    joke_html = requests.get('https://nekdo.ru/random/').text
    joke_text = BeautifulSoup(joke_html, 'lxml').find('div', class_='text').get_text()

    return joke_text


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Я короче умею анекдоты расказывать и погоду предсказывать(если хочешь анекдот напиши: Анекдот, а если погоду, то название города.)',
                           reply_markup=start_keyboard)


@dp.message_handler(text='Анекдот')
async def joke(message: types.Message):
    text = await get_joke()

    await bot.send_message(message.chat.id, text)

open_weather_token = 'fa0456e7c5a170b23b4f0236824c5d7a'

type_weather = {
    "Clear": "Ясно",
    "Clouds": "Облачно",
    "Rain": "Дождь",
    "Drizzle": "Дождь",
    "Thunderstorm": "Гроза",
    "Snow": "Снег ",
    "Mist": "Туман"
}

@dp.message_handler(content_types=["text"])
async def do_something(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        temp = data['main']['temp']

        if data["weather"][0]["main"] in type_weather:
            wd = type_weather[data["weather"][0]["main"]]
        else:
            wd = ""
        if wd == 'Дождь':
            umbrl = 'и возьмите зонт'
        else:
            umbrl = ''
        if temp < -25:
            result = 'Ебать как холодно, сиди дома, дебил.'
        #if temp < 1:
           # result = 'Холодно'
        elif temp < 13:
            result = 'Прохладно'
        elif temp < 17:
            result = 'Прохладненько'
        else:
            result = 'Тепло'

        await bot.send_message(message.from_user.id, f"{result} {umbrl} ({data['main']['temp']}C° {wd})")

    except Exception as ex:
        await bot.send_message(message.from_user.id, "Проверьте название города")


executor.start_polling(dp)

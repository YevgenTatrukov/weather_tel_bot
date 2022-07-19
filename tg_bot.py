import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привіт! Погода в якому місті тебе цікавить?")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        req = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={message}&limit={5}&appid={open_weather_token}"
        )
        data = req.json()
        required_city = data[0]
        lat = required_city["lat"]
        lon = required_city["lon"]

    except:
        await message.reply("\U00002620 Перевірте назву міста \U00002620")

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B",
    }

    try:
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}"
            f"&appid={open_weather_token}&units=metric"
        )
        data = req.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Щось не дуже розумію, а ну глянь у вікно"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed =data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]['sunset'])
        length_of_the_day = sunset_time - sunrise_time
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода у місті {city}\nТемпература: {cur_weather} C° {wd}\n"
              f"Вологість: {humidity}\nТиск: {pressure} мм.рт.ст\n"
              f"Швидкість вітру: {wind_speed} м.с\nСхід сонця: {sunrise_time}\n"
              f"Захід сонця: {sunset_time}\nТривалість дня {length_of_the_day}\n"
              f"***Гарного дня!***")

    except:
        await message.reply("\U00002620 Перевірте назву міста \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)

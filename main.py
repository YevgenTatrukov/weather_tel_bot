import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_city_coordinate(city, open_weather_token):
    try:
        req = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={5}&appid={open_weather_token}"
        )
        data = req.json()
        print("Виберіть яке місто вас цікавить")
        print("-" * 20)
        count = 1
        for i in data:
            print(f"Варіант {count}:")
            print("Країна:", i['country'])
            print("Назва міста:", i['name'])
            try:
                print("Область:", i['state'])
                print("-" * 20)
                print()
            except Exception as ex:
                print(ex)
                print('Нажаль у цього міста немає області')
                print("-" * 20)
                print()
            count += 1
        choice = int(input("Введіть номер варіанту: "))
        print()
        print("+" * 20)
        required_city = data[choice - 1]
        lat = required_city["lat"]
        lon = required_city["lon"]

    except Exception as ex:
        print(ex)
        print("Перевірте назву міста")
    return lat, lon


def get_weather(coordinate, open_weather_token):

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
            f"https://api.openweathermap.org/data/2.5/weather?lat={coordinate[0]}&lon={coordinate[1]}"
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
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода у місті {city}\nТемпература: {cur_weather} C° {wd}\n"
              f"Вологість: {humidity}\nТиск: {pressure} мм.рт.ст\n"
              f"Швидкість вітру: {wind_speed} м.с\nСхід сонця: {sunrise_time}\n"
              f"Захід сонця: {sunset_time}\nТривалість дня {length_of_the_day}\n"
              f"Гарного дня!")
        print("+" * 20)

    except Exception as ex:
        print(ex)
        print("Перевірте назву міста")


def main():
    city = input("Вкажіть місто: ")
    coordinate = get_city_coordinate(city, open_weather_token)
    get_weather(coordinate, open_weather_token)


if __name__ == "__main__":
    main()

import logging
from collections import Counter

from datetime import datetime, timedelta
from enum import Enum
from pprint import pprint
from time import time, sleep
from typing import Any, Tuple

import requests
import json
import time

logging.basicConfig(filemode='application.log', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def wind_duration(deg):
    """Преобразование направления ветра в градусах в направления розы ветров"""
    patterns = {
        'С': 0,
        'СВ': 45,
        'В': 90,
        'ЮВ': 135,
        'Ю': 180,
        'ЮЗ': 225,
        'З': 270,
        'СЗ': 315
    }
    for duration, degree in patterns.items():
        if abs(deg - degree) <= 45 / 2:
            return duration


class WeatherType(Enum):
    # Погода на текущий момент
    CURRENT = 1
    # Прогноз на 5 дней вперед
    PREDICT = 2
    # Детальный прогноз(поминутный/почасовой/по дням)
    DETAIL = 3


class WeatherCache:
    """Кеш данных о погоде"""
    DEFAULT_CACHE_LIFETIME = timedelta(hours=1)

    def __init__(self, lifetime=None):
        self.__data = {}
        self.__last_update = datetime.now()
        self.__lifetime = lifetime or self.DEFAULT_CACHE_LIFETIME

    def __invalidate(self, key: str):
        if key in self.__data:
            logger.info(f'Deleted key {key}')
            del self.__data[key]

    def exists(self, key):
        """Проверить существование ключа"""
        return key in self.__data

    def get(self, key: str):
        """Получить данные из кеша"""
        if datetime.now() - self.__last_update > self.__lifetime:
            # Данные не актуальны, вызвающий метод должен заполнить кеш
            self.__invalidate(key)
        return self.__data.get(key)

    def set(self, key: str, value: Any):
        """Установить данные в кеш"""
        if key in self.__data:
            logger.info('Key exists')
        self.__data[key] = value
        self.__last_update = datetime.now()


class WeatherManager:
    """Класс для получение погоды через API OpenWeather"""
    WEATHER_API_HOST = 'https://api.openweathermap.org'
    WEATHER_API_KEY = 'f3b85666c8661de5228bd6aef6f13458'

    def __init__(self):
        # Два кеша для текущей погоды и для прогноза
        self.__cache = {
            WeatherType.CURRENT: WeatherCache(timedelta(minutes=5)),
            WeatherType.PREDICT: WeatherCache()
        }

    def __get_request_address(self, w_type=WeatherType.CURRENT) -> str:
        """Вернет адресс АПИ для запроса"""
        if w_type is WeatherType.CURRENT:
            request_type = 'weather'
        elif w_type is WeatherType.PREDICT:
            request_type = 'forecast'
        elif w_type is WeatherType.DETAIL:
            request_type = 'onecall'
        else:
            raise ValueError('Unknown weather type')
        return f'{self.WEATHER_API_HOST}/data/2.5/{request_type}'

    def __get_weather_data(self, w_type, **kwargs) -> 'json':
        """
         Получение погоды из API
        :arg kwargs - словарь параметров для запроса
        :arg w_type - тип запроса погоды
        :returns json объект API
            CURRENT - https://openweathermap.org/current
            PREDICT - https://openweathermap.org/forecast5
        """
        logger.info('Getting from API')
        call_params = {
            'appid': self.WEATHER_API_KEY,  # АПИ ключ
            'lang': 'ru',  # Для описания на русском
            'units': 'metric'  # для темпереатуры в градусах Цельсия
        }
        if w_type is WeatherType.DETAIL:
            call_params['exclude'] = ','.join(['minutely', 'daily', 'alerts', 'hourly'])
        try:
            response = requests.get(self.__get_request_address(w_type), params={**kwargs, **call_params})
            logger.debug(response.url)
        except requests.RequestException as ex:
            logger.warning(f'An request error occurred during the request. Details: {ex}')
            raise ex from None
        except Exception as ex:
            logger.warning(f'An unknown error occurred during the request. Details: {ex}')
            raise ex from None
        if response and response.status_code == 200:
            return response.json()
        logger.warning(
            f'Request returned a code different from 200. Code: {response.status_code}. Details: {response.content}'
        )
        raise RuntimeError('Request returned a code different from 200')

    def __parse_data_from_response(self, response, w_type, days=None) -> 'json':
        """
        Получим необходимые данные из ответа
        :arg response - json данных о погоде
        :arg w_type - тип получения погоды(текущая/прогноз)
        :arg days - количество дней для прогноза
        :returns распарсеные данные для отображения
        """
        if w_type is WeatherType.CURRENT:
            return self.__parse_data_current(response)
        elif w_type is WeatherType.PREDICT:
            return self.__parse_data_days(response)
        elif w_type is WeatherType.DETAIL:
            raise NotImplemented('WeatherType.DETAIL not supported')
        else:
            raise ValueError('Unknown weather type')

    @staticmethod
    def __parse_data_current(response):
        # TODO Описание ключей weather и иконки для картинок можно взять https://openweathermap.org/weather-conditions
        return {
            'temp': response['main']['temp'],
            'cloudiness': response['clouds']['all'],
            'humidity': response['main']['humidity'],
            'pressure': response['main']['pressure'],
            'wind': {
                'speed': response['wind']['speed'],
                'deg': response['wind']['deg'],
                'duration': wind_duration(response['wind']['deg'])
            },
            'weather': response['weather']
        }

    @staticmethod
    def __parse_data_days(response):
        _T = lambda t: time.strptime(t, '%H:%M:%S')
        empty_mc = [((None, None, None), None)]
        output = {}
        list_ = response['list']
        logger.debug(json.dumps(response))
        # Сгрупперуем данные по дням. В итоге получим словарь,
        #  где ключом является дата, а внутри содержит прогноз по времени
        for weather_obj in list_:
            datetime_ = datetime.strptime(weather_obj['dt_txt'], '%Y-%m-%d %H:%M:%S')
            date_ = datetime_.date().strftime('%Y-%m-%d')
            time_ = datetime_.time().strftime('%H:%M:%S')
            output[date_] = output.get(date_) or {}
            output[date_].setdefault('list', [])
            output[date_]['list'].append({
                'dt_txt': weather_obj['dt_txt'],
                'time': time_,
                'temp': weather_obj['main']['temp'],
                'cloudiness': weather_obj['clouds']['all'],
                # Интересуют только осадки(гром?)
                'precipitation': [obj for obj in weather_obj['weather'] if
                                  obj['main'] in ('Snow', 'Rain', 'Thunderstorm')],
                'weather': weather_obj['weather']
            })
            # Заполним погоду на утро/день/вечер
            # morning_temp_list = [item["main"]["temp"] for item in ]
            output[date_].setdefault('morning', [])
            output[date_]['morning'].extend(
                [{**w, "temp": weather_obj['main']['temp']} for w in weather_obj['weather']
                 if _T('03:00:00') < _T(time_) < _T('12:00:00')]
            )
            output[date_].setdefault('day', [])
            output[date_]['day'].extend(
                [{**w, "temp": weather_obj['main']['temp']} for w in weather_obj['weather']
                 if _T('12:00:00') <= _T(time_) <= _T('18:00:00')]
            )
            output[date_].setdefault('evening', [])
            output[date_]['evening'].extend(
                [{**w, "temp": weather_obj['main']['temp']} for w in weather_obj['weather']
                 if _T('18:00:00') < _T(time_) < _T('23:00:00') or _T('00:00:00') <= _T(time_) <= _T('03:00:00')]
            )
        # Заполним макс/мин температуры за день
        for date_ in output.keys():
            output[date_]['max_temp'] = max([obj['temp'] for obj in output[date_]['list']])
            output[date_]['min_temp'] = min([obj['temp'] for obj in output[date_]['list']])
            # Будем считать погоду на время суток, как самаую частую по интервалам в это время суток
            #  в виде кортежа (main, desc, icon)
            output[date_]['main_weather'] = {}
            morning_weather_most = (Counter(
                (item['main'], item['description'], item['icon']) for item in output[date_]['morning']).most_common(1)
                or empty_mc)[0]
            output[date_]['main_weather']['morning'] = {
                "main": morning_weather_most[0][0],
                "description": morning_weather_most[0][1],
                "icon": morning_weather_most[0][2],
                "temp": sum(item["temp"] for item in output[date_]['morning']) / (len(output[date_]['morning']) or 1)
            }

            morning_day_most = (Counter(
                (item['main'], item['description'], item['icon']) for item in output[date_]['day']).most_common(1)
                or empty_mc)[0]
            output[date_]['main_weather']['day'] = {
                "main": morning_day_most[0][0],
                "description": morning_day_most[0][1],
                "icon": morning_day_most[0][2],
                "temp": sum(item["temp"] for item in output[date_]['day']) / (len(output[date_]['day']) or 1)
            }

            morning_evening_most = (Counter(
                (item['main'], item['description'], item['icon']) for item in output[date_]['evening']).most_common(1)
                or empty_mc)[0]
            output[date_]['main_weather']['evening'] = {
                "main": morning_evening_most[0][0],
                "description": morning_evening_most[0][1],
                "icon": morning_evening_most[0][2],
                "temp": sum(item["temp"] for item in output[date_]['evening']) / (len(output[date_]['evening']) or 1)
            }

        return output

    @staticmethod
    def __get_coord_by_name(name: str) -> Tuple[float, float]:
        """По названиею города вернет координаты его географического центра"""
        raise NotImplemented("__get_coord_by_name not implemented")

    @staticmethod
    def __get_data_count(data, cnt):
        """Вернет словарь с первыми cnt ключами, где ключи отсортированы по возрастанию"""
        logger.info(f'Adding first {cnt} items')
        keys = list(sorted(data.keys()))[0:cnt]
        return {
            key: value
            for key, value in data.items()
            if key in keys
        }

    def get_for_city(self, city_name: str, w_type=WeatherType.CURRENT, days=None) -> 'json':
        """
        Получение данных о погоде для города
        :arg city_name - город
        :arg w_type - тип получения погоды(текущая/прогноз)
        :arg days - количество дней для прогноза
        :returns распарсеные данные для отображения
        Для текущего прогноза:
        {
            temp: float,  # текущаяя темепратура
            cloudiness: int,  # облачность в %
            humidity: int,  # влажность в %
            wind: {  # ветер
                speed: int,  # скорость в м/с
                deg: int  # направление в градусах
                duration: str  # роза ветров
            },
            weather: [  # Описание погоды
                {
                    id: int, # внутренний идентификатор АПИ
                    main: str, # вид погоды
                    description: str, # описание значения
                    icon: str, # название иконки
                },
                ...
            ]
        }
        Предсказание по часам:
        {
            date_1: {  # Дата
                min_temp: float,  # Минимальная температура за день
                min_temp: float,  # Максимальная температура за день
                list: [  # Подробное описание по часам(с интервалом 3 часа)
                    {
                        dt_txt: str  # ДатаВремя в виде строки
                        time: str,  # Время
                        temp: float,  # Температура
                        cloudiness: int,  # облачность в %
                        precipitation: [  # Осадки
                            {
                                main: main,  # Тип осадков(дождь, снег и т.д.)
                                description: str  # Описание
                            }
                        ],
                        weather: [  # Описание погоды
                            {
                                id: int, # внутренний идентификатор АПИ
                                main: str, # вид погоды
                                description: str, # описание значения
                                icon: str, # название иконки
                            },
                            ...
                        ]
                    },
                    ...
                ],
                morning: [  # Погода на утро (по часам)
                    {
                        id: int, # внутренний идентификатор АПИ
                        main: str, # вид погоды
                        description: str, # описание значения
                        icon: str, # название иконки
                    },
                    ...
                ],
                day: [  # Погода на день (по часам)
                    {
                        id: int, # внутренний идентификатор АПИ
                        main: str, # вид погоды
                        description: str, # описание значения
                        icon: str, # название иконки
                    },
                    ...
                ],
                evening: [  # Погода на вечер (по часам)
                    {
                        id: int, # внутренний идентификатор АПИ
                        main: str, # вид погоды
                        description: str, # описание значения
                        icon: str, # название иконки
                    },
                    ...
                ],
                main_weather: {  # Сгруппирования погода на весь промежуток (утро/день/вечер)
                    morning: [
                        # Список из кортежа и числа(кол-во вхождений)
                        # Кортеж - поля из объекта weather АПИ
                        [(main, description, icon), int]
                    ],
                    day: [],
                    evening: []
                }
            },
            date_2: {...},
            ...
            date_5: {...}
        }
        """
        if w_type is WeatherType.DETAIL:
            lon, lat = self.__get_coord_by_name(city_name)
        if self.__cache[w_type].exists(city_name):
            logger.info('Getting from cache')
            parsed_data = self.__cache[w_type].get(city_name)
            if w_type is WeatherType.PREDICT and days:
                return self.__get_data_count(parsed_data, days)
        json_data = self.__get_weather_data(w_type, q=city_name)
        parsed_data = self.__parse_data_from_response(json_data, w_type)
        self.__cache[w_type].set(city_name, parsed_data)
        if w_type is WeatherType.PREDICT and days:
            return self.__get_data_count(parsed_data, days)
        return parsed_data


if __name__ == '__main__':
    wm = WeatherManager()
    res1 = wm.get_for_city('Yaroslavl', WeatherType.PREDICT, 3)
    pprint(res1)
    res2 = wm.get_for_city('Yaroslavl', WeatherType.PREDICT)
    pprint(res2)
    print(res1 == res2)

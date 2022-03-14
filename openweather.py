import requests
import json
import logging
from config_file import ConfigFile


class WeatherData:

    def __init__(self):
        self.outdoor_temperature: float = 0.0
        self.cloudiness: float = 0.0


class OpenWeather:

    def __init__(self, cfg: ConfigFile):
        self.apiKey = cfg.WEATHER_API_KEY
        self.cityId = cfg.WEATHER_CITYID

    def get_outdoor_temperature(self):

        request = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(self.cityId) \
            + '&appid=' + str(self.apiKey) \
            + '&units=metric'
        try:
            response = requests.get(request)
            if response.status_code == 200:
                # successful request
                data = response.json()
                return data['main']['temp']
            else:
                logging.critical('Could not read Weather Data')
        except:
            logging.critical('Could not read Weather Data')

    def get_weather_data(self) -> WeatherData:

        weather_data = WeatherData()

        request = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(self.cityId) \
            + '&appid=' + str(self.apiKey) \
            + '&units=metric'
        try:
            response = requests.get(request)
            if response.status_code == 200:
                # successful request
                data = response.json()
                weather_data.outdoor_temperature = data['main']['temp']
                weather_data.cloudiness = data['clouds']['all']
            else:
                logging.critical('Could not read Weather Data')
        except:
            logging.critical('Could not read Weather Data')

        return weather_data

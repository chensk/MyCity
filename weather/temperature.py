#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5
import abc
import collections
import datetime
import json
import requests

from MyCity.exception import *


class Temperature:
    @abc.abstractmethod
    def get_temperature(self, date, city, country):
        pass


class OpenWeatherTemperature(Temperature):
    """
    implements Temperature using apis of "openweathermap.org"
    Deprecated.
    """
    def __init__(self):
        app_id = "3db0b42d7b4e3a4dda8a10d58e7ffb14"
        self.url = "http://api.openweathermap.org/data/2.5/weather?" \
                   "q={city},{country}&units=metric&APPID="+app_id

    def get_temperature(self, date, city, country):
        # verify argument
        if date > datetime.datetime.today():
            raise WeatherServiceException("Only historical data accessible")
        Temp = collections.namedtuple('Temp', ['min', 'max'])
        res = requests.get(self.url.format(**{"city":city, "country":country}))
        if res.status_code != 200:
            raise WeatherServiceException("Error in getting weather data: "
                                          + res.text.get("message", "network fails"))
        result = json.loads(res.text)
        return Temp(max=result['main']['temp_max'], min=result['main']['temp_min'])

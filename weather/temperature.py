#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5
import abc
import collections
import lxml.html
import json
import requests

from MyCity.exception import *
from MyCity.util import *

Temp = collections.namedtuple('Temp', ['min', 'max'])

class Temperature:
    @abc.abstractmethod
    def get_temperature(self, date, city, country):
        pass


class OpenWeatherTemperature(Temperature):
    """
    Implements Temperature using apis of "openweathermap.org"
    Deprecated.
    """
    def __init__(self):
        app_id = "3db0b42d7b4e3a4dda8a10d58e7ffb14"
        self.url = "http://history.openweathermap.org/data/2.5/history/city?" \
                   "q={city},{country}&type=hour&start={start}&end={end}"

    def get_temperature(self, date, city, country):
        date = format_date(date)
        # verify argument
        if date > datetime.datetime.today():
            raise WeatherServiceException("Only historical data accessible")
        res = requests.get(self.url.format(**{"city":city, "country":country}))
        if res.status_code != 200:
            raise WeatherServiceException("Error in getting weather data: "
                                          + res.text.get("message", "network fails"))
        result = json.loads(res.text)
        return Temp(max=result['main']['temp_max'], min=result['main']['temp_min'])


class TianqiTemperature(Temperature):
    """
    Implements Temperature using apis of "tianqi.com"
    """
    def __init__(self):
        self.url = "http://lishi.tianqi.com/{city}/{date}.html"

    def get_temperature(self, date, city, country):
        date = format_date(date)
        # verify argument
        if date > datetime.datetime.today():
            raise WeatherServiceException("Only historical data accessible")
        res = requests.get(self.url.format(**{"city":city, "date":date.strftime("%Y%m")}))
        day = date.day
        if res.status_code != 200:
            raise WeatherServiceException("Error in getting weather data: "
                                          + res.text.get("message", "network fails"))
        parser = lxml.html.fromstring(res.text)
        try:
            max_temperature = int(parser.xpath(
                '//*[@id="tool_site"]/div[2]/ul[{}]/li[2]/text()'.format(day+1))[0])
            min_temperature = int(parser.xpath(
                '//*[@id="tool_site"]/div[2]/ul[{}]/li[3]/text()'.format(day+1))[0])
        except IndexError:
            raise WeatherServiceException("Error in parsing weather data")
        return Temp(min=min_temperature, max=max_temperature)

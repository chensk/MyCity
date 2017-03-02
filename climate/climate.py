#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/3/2
import collections
import datetime

import lxml.html
import pypinyin
import util
from exception import *


class CityClimate:
    """
    class that provides services about climate of specified city
    """

    def __init__(self, city):
        """
        initialize using name of city.
        """
        self.city_in_Chinese = city
        self.city_in_pinin = "".join(pypinyin.lazy_pinyin(city)).lower()
        self.weather_url = "http://lishi.tianqi.com/{}".format(self.city_in_pinin) + "/{}.html"
        self.aqi_url = "https://www.aqistudy.cn/historydata/daydata.php?city={}".format(self.city_in_Chinese)
        self.__cache = {}

    def get_climate(self, date):
        """
        return climate of the specified date
        :param date: datetime instance or tuple containing
        year, month and day i.e. (XXXX, XX, XX)
        :return: the climate data encapsulated in dictionary
        """
        try:
            date = datetime.datetime(*date)
        except TypeError:
            if not isinstance(date, datetime.datetime):
                raise WeatherServiceException("date format error")
        if date in self.__cache:
            return self.__cache[date]
        climate = {}.fromkeys(["temperature", "weather", "air quality"])
        crawler = util.Crawler()
        date_formatted = date.strftime("%Y%m")
        # crawl weather data from tianqi.com
        response = crawler.crawl(self.weather_url.format(date_formatted), charset="gbk")
        climate['temperature'], climate['weather'] = self.extract_climate_data(response, date)
        # crawl aqi data from aqistudy.cn
        response = crawler.crawl(self.aqi_url + "&month={}".format(date_formatted))
        climate['aqi'] = self.extract_aqi_data(response, date)
        self.__cache[date] = climate
        return climate

    @staticmethod
    def extract_climate_data(text, date):
        Temperature = collections.namedtuple('Temperature', ['min', 'max'])
        Weather = collections.namedtuple('Weather', ['weather'])
        parser = lxml.html.fromstring(text)
        try:
            day = date.day
            max_temperature = int(parser.xpath(
                '//*[@id="tool_site"]/div[2]/ul[{}]/li[2]/text()'.format(day + 1))[0])
            min_temperature = int(parser.xpath(
                '//*[@id="tool_site"]/div[2]/ul[{}]/li[3]/text()'.format(day + 1))[0])
            weather = parser.xpath(
                '//*[@id="tool_site"]/div[2]/ul[{}]/li[4]/text()'.format(day + 1))[0]
        except (IndexError, TypeError):
            raise WeatherServiceException("Error in parsing climate data")
        return Temperature(min=min_temperature, max=max_temperature), \
               Weather(weather=weather)

    @staticmethod
    def extract_aqi_data(text, date):
        AQI = collections.namedtuple('aqi', ['aqi', 'level', 'pm2_5'])
        parser = lxml.html.fromstring(text)
        try:
            day = date.day
            aqi = int(parser.xpath(
                '/html/body/div[3]/div[1]/div[1]/table/tr[{}]/td[2]/text()'.format(day + 1))[0])
            pm2_5 = float(parser.xpath(
                '/html/body/div[3]/div[1]/div[1]/table/tr[{}]/td[5]/text()'.format(day + 1))[0])
            level = parser.xpath(
                '/html/body/div[3]/div[1]/div[1]/table/tr[{}]/td[4]/div/text()'.format(day + 1))
        except (IndexError, TypeError):
            raise WeatherServiceException("Error in parsing climate data")
        return AQI(aqi=aqi, level=level, pm2_5=pm2_5)

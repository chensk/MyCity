#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5
import datetime
import pytest
import random
import time
from MyCity.weather import *
from MyCity.exception import *


def test_temperature():
    city=["shenzhen", "shanghai", "hangzhou", "beijing", "chongqing", "tianjin"]
    country="cn"
    today = datetime.datetime.today()
    rand = random.Random()
    temp = OpenWeatherTemperature()
    for _ in range(10):
        test_days = datetime.timedelta(days=rand.randint(0, 100))
        test_date = today - test_days
        city_random = random.choice(city)
        print("test temperature for {} in {}".format(city_random, test_date))
        print("result: ", end="")
        temp.get_temperature(test_date, city_random, country)
        time.sleep(0.1)
    with pytest.raises(WeatherServiceException):
        temp.get_temperature(today+datetime.timedelta(days=1), random.choice(city), country)
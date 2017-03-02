#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5
import datetime
import random
import time

import pytest
from MyCity.climate import *
from MyCity.exception import *


def test_temperature():
    city = ["深圳", "上海", "杭州", "北京", "重庆", "天津"]
    today = datetime.datetime.today()
    rand = random.Random()
    for _ in range(10):
        test_days = datetime.timedelta(days=rand.randint(31, 100))
        test_date = today - test_days
        city_random = random.choice(city)
        climater = CityClimate(city_random)
        print("test temperature for {} in {}".format(city_random, test_date))
        print("result: ", end="")
        print(climater.get_climate(test_date))
        time.sleep(0.1)
    climater = CityClimate(random.choice(city))
    with pytest.raises(WeatherServiceException):
        climater.get_climate(today + datetime.timedelta(days=1))

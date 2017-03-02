#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5


class CityServiceException(Exception):
    pass


class WeatherServiceException(CityServiceException):
    pass


class EconomyServiceException(CityServiceException):
    pass


class BasicServiceException(CityServiceException):
    pass


class NetworkException(CityServiceException):
    pass

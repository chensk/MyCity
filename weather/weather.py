#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5
import abc


class Weather:
    @abc.abstractmethod
    def get_weather(self, date, city, country):
        pass
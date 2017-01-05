#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/1/5
import datetime

def format_date(date):
    if isinstance(date, str):
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        return date
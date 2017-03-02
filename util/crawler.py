#!/usr/bin/env python
# -*- coding: utf8 -*-
# created on 2017/3/2
import requests

from exception import *


class Crawler:
    def __init__(self):
        self.__cache = {}

    def crawl(self, url, headers=None, cookies=None, charset="utf-8"):
        if url in self.__cache:
            return self.__cache[url]
        if not headers:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/56.0.2924.87 Safari/537.36',
                       }
        if cookies:
            response = requests.get(url, headers=headers, cookies=cookies)
        else:
            response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = charset
            self.__cache[url] = response.text
            return response.text
        else:
            raise NetworkException("failure in crawling {}".format(url))

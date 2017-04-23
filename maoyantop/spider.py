#!/usr/bin/python
# coding=utf-8
# -------------------------------------------------------------------------------
# Name:     spider
# Purpose:  Requests+正则表达式
# Version:  python 3.5
#
# Author:   Ang Lee
# Created:  2017.4.23
# History:
# Licence:  <your licence>
# -------------------------------------------------------------------------------
import json

import requests
from requests.exceptions import RequestException
import re

from multiprocessing import Pool


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        # 格式处理
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        # 中文乱码
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])

# Question:多进程重复抓取问题

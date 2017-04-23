#!/usr/bin/python
# coding=utf-8
# -------------------------------------------------------------------------------
# Name:     spider
# Purpose:  分析Ajax爬取图片
# Version:  python 3.5
#
# Author:   Ang Lee
# Created:  2017.4.23
# History:
# Licence:  <your licence>
# -------------------------------------------------------------------------------
import json
import re
import os
# python2/3关于urllib使用有区别
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pymongo
from config import *
from hashlib import md5
from multiprocessing import Pool
from json import JSONDecodeError
# 不加connect会提示mongo连接在fork之前就被创建了
# 解决方案：connect=False参数
# 初始化数据库连接的代码放到fork以后，即在线程里面需要的时候再初始化
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    # 使用urlencode为数组解析成get参数
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('请求索引页---成功', url)
            return response.text
        return None
    except RequestException:
        print('请求索引页失败')
        return None


def parse_page_index(html):
    try:
        # json.loads()函数直接将json数据解析成python字典
        # data.keys()可以获取所有的键
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('请求详情页---成功', url)
            return response.text
        return None
    except RequestException:
        print('请求详情页失败', url)
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    # script中的信息无法使用bs4这样的解析器来解析，所以直接使用正则去匹配
    images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def sava_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MONGO---成功', result)
        return True
    print('MONGO失败', result)
    return False


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('请求图片---成功', url)
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片失败', url)
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            print(result)
            if result:
                sava_to_mongo(result)
    pass


if __name__ == '__main__':
    groups = [x * 20 for x in range(GROUP_START, GROUP_END+1)]
    pool = Pool()
    pool.map(main, groups)

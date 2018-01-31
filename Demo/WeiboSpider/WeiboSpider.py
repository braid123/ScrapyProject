#!/usr/bin/env python
# -*- coding:utf-8 -*-
# python version :3.6

import requests
import urllib
from bs4 import BeautifulSoup
from DownLoadHtml import download_func
from urllib import parse
from urllib.parse import quote
import json
import time
"""
http://s.weibo.com/user/%25E5%258D%25B3%25E5%2588%25BB&Refer=index
%25E5%258D%25B3%25E5%2588%25BB
http://s.weibo.com/user/

webdriver来登录微博获取cookie,设置过期时间6hours,未过期则去本地读取。
否则重新登录获取cookie，获取cookie后则分析微博网页端的请求，
找到相应接口和参数，然后去请求我们要的数据

search_person = urllib.parse.quote(search_name)
# sina网站上采取的quote两次的方法
search_url = search_url + str(search_person) + '&Refer=index'
print("search_url>>>", search_url)
html = download_func(search_url)
page = BeautifulSoup(html, 'lxml')
print("page>>>", page)
data = requests(search_url).text
jsondata = json.loads(data)
print(data, jsondata)
search_Items = page.find_all(attrs={"class": "list_person clearfix"})
print("search_Items>>>", search_Items)

"""


def get_timestamp():
    # 获取当前系统时间戳
    try:
        tamp = time.time()
        timestamp = str(int(tamp)) + "000"
        print(timestamp)
        return timestamp
    except Exception as e:
        print(e)
    finally:
        pass

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import re
import selenium.webdriver.support.ui as ui
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = ui.WebDriverWait(browser, 10)
search_url = 'http://s.weibo.com'
search_name = input("Input the person you want to follow")


# 请求首页
def search():
    print('Start Search')
    try:
        browser.get('http://s.weibo.com/')
        data = browser.title
        print(data)
        # 点击找人
        browser.find_element_by_xpath('//*[@id="pl_searchHead"]/div[1]/ul/li/a[3]').click()
        input = wait.until(
            # 浏览器在搜索框copy selector
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#pl_searchHead > div.search_head_formbox \
                                            > div > div > div.searchInp_box > div > input'))
        )
        # 按钮被点击
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        '#pl_searchHead > \
                                                        div.search_head_formbox > div > div >\
                                                         div.searchBtn_box > a')))
        # 传参
        input.send_keys(search_name)
        print(search_name)
        submit.click()
        # 等待页面加载出
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           '#pl_user_feedList > \
                                                            div.WB_cardwrap.S_bg2.relative > div.W_pages > a')))
        print(total.text)
        return total.text
    except TimeoutException:
        print("Error time")

import WeiboLogin


def main():
    try:
        weibo = WeiboLogin.WeiBoLogin()
        search_page = search()
    except Exception as e:
        print('main函数出错', e)
    finally:
        browser.close()

if __name__ == '__main__':
    main()


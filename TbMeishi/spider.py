#!/usr/bin/python
# coding=utf-8
# -------------------------------------------------------------------------------
# Name:     spider
# Purpose:  Selenium+Chrome/PhantomJS抓取淘宝搜索
# Version:  python 3.5
#
# Author:   Ang Lee
# Created:  2017.4.23
# History:
# Licence:  <your licence>
# -------------------------------------------------------------------------------
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo

# browser = webdriver.Chrome(),会调用接口，弹窗Chrome
# 若没有配置PhantomJS的环境变量,需加入executable_path参数
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# 默认窗口较小, 故调整
browser.set_window_size(1366, 768)

wait = WebDriverWait(browser, 10)



# 请求首页
def search():
    print('进入首页')
    try:
        browser.get('https://www.taobao.com')
        # 参考官方文档Explicit Waits
        input = wait.until(
            # 浏览器在搜索框copy selector
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        # 按钮被点击
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        # 传参
        input.send_keys(KEYWORD)
        submit.click()
        # 等待页面加载出
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('进入下一页')
    try:
        # 参考官方文档Explicit Waits
        input = wait.until(
            # 浏览器在搜索框copy selector
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#mainsrp-pager > div > div > div > div.form > input'))
        )
        # 按钮被点击
        submit = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        # 判断当前页面文字在这个元素里, CSS高亮
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                              '#mainsrp-pager > div > div > div > ul > li.item.active > span'),
                                             str(page_number))
        )
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    print('获取商品详情')
    # 先判定item是否加载成功
    # PS: CSS selector 后的符号#不要漏,否则会导致抓取不到,从而循环爬取
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    # 得到html中选择的内容
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('mongo 成功', result)
    except Exception:
        print('mongo 错误', result)


def main():
    try:
        total = search()
        # 提取出总页数
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total+1):
            next_page(i)
    except Exception as e:
        print('main函数出错', e)
    finally:
        browser.close()

if __name__ == '__main__':
    main()

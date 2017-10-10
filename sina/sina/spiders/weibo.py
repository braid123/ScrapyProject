#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import json
from scrapy import Request
import re
import time
from ..items import CommentItem
from urllib import parse
from .control import delay


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["m.weibo.cn"]
    # init_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'

    @delay(3)
    def start_requests(self):
        single_weibo_id = '4160547165300149'
        post_comment_url = 'https://m.weibo.cn/api/comments/show?id=%s&page=1' % single_weibo_id
        yield Request(url=post_comment_url, callback=self.get_comment_content)

    # 获取评论内容
    def get_comment_content(self, response):
        content = json.loads(response.body)
        for data in content.get('data'):
            post_id = re.findall('(\d+)', response.url)[0]
            _id = data.get('id')
            # 将回复后的评论截取出
            text = re.sub('<.*?>', '', data.get('text'))
            text_2 = re.sub(r'.*?@.*?:', '', text)
            reply_text = re.sub('.*?@.*?:', '', re.sub('<.*?>', '', data.get('reply_text', '')))
            item = CommentItem()
            item['_id'] = _id
            item['comment'] = text_2
            item['refer'] = reply_text
            item['post_id'] = post_id
            yield item

        max_page = content.get('max')
        print('max_page is %s ' % max_page)
        page_num_pattern = r'(\d+)'
        page_num = re.findall(page_num_pattern, response.url)[1]
        if int(max_page) > 1 and int(max_page) > int(page_num):
            post_id_pattern = r'.*?id=(\d+)&page=.*?'
            post_id = re.findall(post_id_pattern, response.url)[0]
            url = 'https://m.weibo.cn/api/comments/show?id=%s&page=%s' % (post_id, str(int(page_num) + 1))
            yield Request(url=url, callback=self.get_comment_content)

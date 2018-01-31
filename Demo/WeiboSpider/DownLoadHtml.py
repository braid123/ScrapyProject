#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import urllib.response
import urllib.error


def download_func(url, user_agent='wswp', proxy=None, num_retries=2):
    """Download function with support for proxies"""
    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url,headers=headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download_func(url, user_agent, proxy, num_retries-1)
    return html

if __name__ == '__main__':
    download_func()

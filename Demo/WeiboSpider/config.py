# 使用Phantomjs API
SERVICE_ARGS = []
# 移植性
SERVICE_ARGS.append('--load-images=no')
# 关闭图片加载
SERVICE_ARGS.append('--disk-cache=yes')
# 开启缓存
SERVICE_ARGS.append('--ignore-ssl-errors=true')
# 忽略https错误


headers = {  # User-Agent需要根据每个人的电脑来修改
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 's.weibo.com',
    'Pragma': 'no-cache',
    'Referer': 'http://s.weibo.com/?topnav=1&wvr=6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product'

# 使用Phantomjs API
SERVICE_ARGS = []
# 移植性
SERVICE_ARGS.append('--load-images=no')  #关闭图片加载
SERVICE_ARGS.append('--disk-cache=yes')  #开启缓存
SERVICE_ARGS.append('--ignore-ssl-errors=true') #忽略https错误

# 可替换成其他关键词
KEYWORD = '手表'
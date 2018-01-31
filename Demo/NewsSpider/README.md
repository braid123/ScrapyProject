# NewsSpider

pyinstall暂时不支持Python3.6.


(1)所以需要另外安装,先在python版本指定目录中pip install pyinstaller(eg:D:\Python\Scripts)


(2)等待安装成功之后到https://github.com/pyinstaller/pyinstaller    下载ZIP安装包


(3)解压之后将PyInstaller文件夹复制到指定目录\Lib\site-packages目录下.


(4)需要生成的py程序和ico格式图片（可有可无）放到指定目录文件夹中.


(5)pyinstaller -F -w (-i image.ico) 文件名.py
-F表示打包成一个文件 -w不显示命令行 -i表示图标，图标格式是.ico


(6)打包完成后exe程序在D:\Python\Scripts\dist中，D:\python\Scripts\build中是缓存文件
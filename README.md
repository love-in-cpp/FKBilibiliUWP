FKBilibiliUWP
=======================
  `PYQT5` `BiliBiliUWP` `爬虫` `效率工具`   
  
  基于爬虫和PYQT5的图形用户界面的bilibiliUWP视频重命名+整理工具
## 如何使用？
  [使用说明.pdf](https://github.com/love-in-cpp/FKBilibiliUWP/files/8967723/default.pdf)  

## 未来工作 ~~***（可能）***~~

* [ ] 针对新版加密视频，推出`解密`后再输出的功能  
* [ ] 增加免除用户手动选择输出文件夹的功能  
* [ ] 增加免网络运行功能(~~虽然这个有写md的时间都能做完~~)  
* [ ] 用C#实现，作为IO操作练手的项目 

## 模块功能
* `TitleSpider.py` 用于获取指定的视频名称列表
* `FileOperator.py` 用于完成处理文件（夹）的读取、写入、移动、复制、删除、重命名操作
* `main.py` 用于处理UI的信号和槽
* `MainWindow.py` 负责部分固定UI的生成，该文件由 `pyuic5.exe` 作用在 `MainWindow.ui` 上转化而来 
* `icon.py` 由`.icon`文件使用`icon2py.py`生成
```Python
import base64

open_icon = open("FKBili.png", "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = write_data = "img = %s" % b64str
f = open("icon.py", "w+")
f.write(write_data)
f.close()
```

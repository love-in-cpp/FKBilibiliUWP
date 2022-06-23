FKBilibiliUWP
=======================
  `PYQT5` `BiliBiliUWP` `爬虫` `效率工具`   
  
  基于爬虫和PYQT5的图形用户界面的bilibiliUWP视频重命名+整理工具
## 如何使用？
  [使用说明.pdf](https://github.com/love-in-cpp/FKBilibiliUWP/files/8967723/default.pdf)  

## 未来工作 ~~***（可能）***~~

* [ ] 针对新版加密视频，推出`解密`后再输出的功能  
* [ ] 增加免除用户**手动选择输出文件夹**的功能  
* [ ] 增加**免网络**运行功能(~~虽然这个有写md的时间都能做完~~)  
* [ ] 用 ``C#`` 实现，作为IO操作练手的项目 

## 界面截图
![image](https://user-images.githubusercontent.com/59083942/175336107-07e9105b-483d-4d4b-a081-54ab78cb21a2.png)
![image](https://user-images.githubusercontent.com/59083942/175336254-3a883510-5f75-4099-aac8-0590cddbaa93.png)

## 模块功能
* `TitleSpider.py` 用于获取指定的视频名称列表
* `FileOperator.py` 用于完成处理文件（夹）的读取、写入、移动、复制、删除、重命名操作
* `main.py` 用于处理UI的信号和槽以及多线程
* `MainWindow.py` 负责部分固定UI的生成，该文件由 `pyuic5.exe` 作用在 `MainWindow.ui` 上生成
* `icon.py` 由`icon2py.py` 作用在 `.icon`文件上生成
  ```Python
  # icon2py.py
  import base64
  
  open_icon = open("FKBili.png", "rb")
  b64str = base64.b64encode(open_icon.read())
  open_icon.close()
  write_data = write_data = "img = %s" % b64str
  f = open("icon.py", "w+")
  f.write(write_data)
  f.close()
  ```

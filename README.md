FKBilibiliUWP
=======================
  `PYQT5` `BiliBiliUWP` `爬虫` `效率工具`   
  
  基于爬虫和PYQT5的图形用户界面的bilibiliUWP视频重命名+整理工具

没有`bilibiliUWP 2.14.71`版本的点这里:[[阿里云链接]2.14.71版本+工具 ](https://www.aliyundrive.com/s/NxkGviXv4aD "点击跳转")

## 如何使用？
  

## 未来工作 ~~***（可能）***~~

* [ ] 针对新版加密视频，推出`解密`后再输出的功能  
* [x] 增加免除用户**手动选择输出文件夹**的功能  (***状态：Done***) 
* [x] 增加**免网络**运行功能(~~虽然这个功能有写这个md的时间都能做完~~)  (***状态：Done***) 
* [ ] 用 ``C#`` 实现，作为IO操作练手的项目

## 界面截图


## 效果截图
  程序正确执行后，会在选择的输出文件夹的**目录下**，自动创建一个视频标题名称的子文件夹，整理后的视频存放在子文件夹中。


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

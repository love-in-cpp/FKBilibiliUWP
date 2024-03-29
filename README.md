FKBilibiliUWP
=======================
  `PYQT5` `BiliBili UWP` `爬虫` `效率工具`   
  
  基于爬虫（可选）、IO和PYQT5图形用户界面的bilibiliUWP视频`解密`+重命名+整理工具

`bilibiliUWP 2.14.79`官方最新版本和本工具、使用文档可直接点这里:   
[[阿里云链接]工具+文档 ](https://www.aliyundrive.com/s/XjD25zFVRLa "点击跳转")   
[[蓝奏云链接]2.14.79版本+工具+文档 ](https://wwb.lanzoul.com/b037845ud "点击跳转")（密码:51n7）  
[[百度云链接]2.14.79版本+工具+文档 ](https://pan.baidu.com/s/16oJzhc0kv9Z____DENFpRw?pwd=1111 "点击跳转")（提取码：1111）



## 如何使用？
[V4.5 使用文档（高清版）.pdf](https://github.com/love-in-cpp/FKBilibiliUWP/files/9201187/V4.4.pdf)


## 未来工作

* [x] 针对新版加密视频，推出`解密`后再输出的功能   (***状态：Done***) 
* [x] 增加记忆输出文件夹的功能，该功能将为**安装版专属**，因为绿色版执行结束后不会在用户不知情的情况下保留任何文件。(***状态：Done***) 
* [x] 增加免除用户**手动选择输出文件夹**的功能  (***状态：Done***) 
* [x] 增加**免网络**运行功能(~~虽然这个功能有写这个md的时间都能做完~~)  (***状态：Done***) 
* [ ] 有空学了python的面向对象后，运用设计模式重构代码

## 界面截图
![img](https://user-images.githubusercontent.com/59083942/175548393-19469586-5fbb-4db7-9fd8-0682a568f52a.png)
![img_1](https://user-images.githubusercontent.com/59083942/175548400-effc0ebc-4866-40a7-a477-a5453433b164.png)


## 效果截图
  程序正确执行后，会在选择的输出文件夹的**目录下**，自动创建一个视频标题名称的子文件夹，整理后的视频存放在子文件夹中。
  ![img_2](https://user-images.githubusercontent.com/59083942/175548412-ba1abde2-55a1-4829-9ba9-b885dc7bc020.png)


## 模块功能
* `TitleSpider.py` 用于获取指定的视频名称列表
* `FileOperator.py` 用于完成处理文件（夹）的读取、写入、移动、复制、删除、重命名、筛选操作
* `main.py` 用于处理UI的信号和槽以及多线程
* `MainWindow.py` 负责部分固定UI的生成，该文件由 `pyuic5.exe` 作用在 `MainWindow.ui` 上生成
* `icon.py` 由`icon2py.py` 作用在 `.icon`文件上生成

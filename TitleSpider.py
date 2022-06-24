# -*- coding = utf-8 -*-
# @Time : 2022/6/21 15:33
# @Author : 刘正阳
# @File : TitleSpider.py
# @Software : PyCharm
import os

import requests
import re
from bs4 import BeautifulSoup

findLink = re.compile(r'"part":"(.*?)","duratio')

global fileName


# 获取网页数据，传入参数：网址
def FinData(url):
    dataList = []
    getUrl = requests.get(url=url)
    bsHtml = BeautifulSoup(getUrl.text, "html.parser")
    urlTitleList = bsHtml.get_text().title().split('\n', 1)
    urlTitle = urlTitleList[0][:-30].lstrip()
    # dataList.append(str(urlTitle))
    bsFinData = bsHtml.select('script')
    bsData = ''

    # 筛选列表数据
    for i in bsFinData:
        bsData = str(i)
        if 'window.__INITIAL_STATE__={' in bsData:
            break

    # 正则查找，返回列表
    reList = re.findall(findLink, bsData)
    dataList += reList

    return dataList, urlTitle


def saveAsTxt(video_list, urlTitle, path):
    fileTitle = urlTitle + ".txt"  # 合成.txt格式 文件名
    for s in fileTitle:
        cut = ['|', '\\', '/', ':', '?', '"', '<', '>']
        if s in cut:
            fileTitle = fileTitle.replace(s, ' ')

    fileTitle = os.path.join(path, fileTitle)
    # 去除标题中的Windows不兼容的的命名字


    nameFile = open(fileTitle, "w", encoding="utf-8")  # 写入文件
    j = 0
    for i in video_list:
        j += 1
        nameFile.write(i + "\n")
    nameFile.close()
    return fileTitle


def GetTxt(bid, path):
    global fileName
    urlPart = 'https://www.bilibili.com/video/'
    bv = bid
    url = urlPart + bv

    dataList, urlTile = FinData(url)

    fileName = saveAsTxt(dataList, urlTile, path)

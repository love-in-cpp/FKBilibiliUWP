# -*- coding = utf-8 -*-
# @Time : 2022/6/22 12:29
# @Author : 刘正阳
# @File : FileOperator.py
# @Software : PyCharm
import os
import re
import shutil

'''
传入path值，读取当前path一级目录下的.dvi文件，返回[isDviFounded,bid,aid,title]列表
'''
global file_name


def GetDviInfo(path):
    isDviFounded = False
    file_type = '.dvi'
    dviFile = None
    bid = None
    aid = None
    title = None
    description = None

    filelist = os.listdir(path)
    for file in filelist:
        if file_type in file:
            isDviFounded = True
            dviFile = os.path.join(path, file)

    if isDviFounded is False:
        return [isDviFounded, bid, aid, title]
    else:
        with open(dviFile, encoding='UTF-8') as f:
            lines = f.readlines()
            s = str(lines[0])

            findBid = re.compile(r'"Bid":"(.*?)"')
            findDviTitle = re.compile(r'"Title":"(.*?)"')
            findAid = re.compile(r'"Aid":"(.*?)"')

            bid = re.findall(findBid, s)[0]
            aid = re.findall(findAid, s)[0]
            title = re.findall(findDviTitle, s)[0]
            for s in title:
                cut = ['|', '\\', '/', ':', '?', '"', '<', '>']
                if s in cut:
                    title = title.replace(s, ' ')
            return [isDviFounded, bid, aid, title]


def FindAllMp4Files(path):
    fileTypeList = ['mp4', 'MP4', 'mP4', 'Mp4']
    fileList = []  # 存储要copy的文件全名
    fileNamelist = []
    for dirPath, dirNames, fileNames in os.walk(path):
        for file in fileNames:
            fileType = file.split('.')[-1]
            if fileType in fileTypeList:
                file_fullname = os.path.join(dirPath, file)  # 文件全名
                fileList.append(file_fullname)
                fileNamelist.append(file)
    return [fileList, fileNamelist]


# return fileList
def CopyFile(srcFileList, dstFolder):
    for file in srcFileList:
        shutil.copy(file, dstFolder)


def MoveFile(srcFileList, dstFolder):
    for file in srcFileList:
        shutil.move(file, dstFolder)


# 排序用到的key
def get_series(dataList):
    return int(dataList.split('_')[1])


def DoRename(path, fileName):
    # 获取文件名
    filName = fileName

    # 读取该文件
    with open(filName, encoding='UTF-8') as f:
        lines = f.readlines()  # 新文件名按行保存

    fileList = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）

    fileList.sort(key=get_series)

    i = 1
    for files in fileList:  # 遍历所有文件
        oldDir = os.path.join(path, files)  # 原来的文件路径
        if os.path.isdir(oldDir):  # 如果是文件夹则跳过
            continue
        filetype = os.path.splitext(files)[1]  # 文件扩展名
        newDir = os.path.join(path, str(i) + '. ' + lines[i].strip('\n') + filetype)  # 新的文件路径
        os.rename(oldDir, newDir)  # 重命名
        i = i + 1


def DeleteTxt(delDir, delName):
    delList = os.listdir(delDir)
    for f in delList:
        if f == delName:
            filePath = os.path.join(delDir, f)
            if os.path.isfile(filePath):
                os.remove(filePath)


def DeleteDir(delDir):
    os.system(f"attrib -r {delDir}")
    shutil.rmtree(delDir, True)


def RenameDir(name):
    os.rename()

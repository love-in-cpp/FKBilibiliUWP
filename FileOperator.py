# -*- coding = utf-8 -*-
# @Time : 2022/6/22 12:29
# @Author : 刘正阳
# @File : FileOperator.py
# @Software : PyCharm
import os
import random
import re
import shutil

'''
传入path值，读取当前path一级目录下的.dvi文件，返回[isDviFounded,bid,aid,title]列表
'''
global localFileName


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


def GetFileSeries(fileList):
    return int(fileList.split('\\')[-2])


def FindAllMp4Files(path):
    # 这里是不需要对输出结果排序的，因为在移动这些文件后，DoRename调用被移动的文件，会排好序
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
def GetSeries(dataList):
    return int(dataList.split('_')[-2])


def DoRename(path, fileName, aID):
    # 获取.txt文件名
    filName = fileName
    # 读取.txt文件
    with open(filName, encoding='UTF-8') as f:
        lines = f.readlines()  # 新文件名按行保存

    # 提取出含有指定特征的fileList
    fileTypeList = ['mp4', 'MP4', 'mP4', 'Mp4']
    fileList = []  # 存储要copy的文件全名
    # 获取要被命名的文件，包含了文件夹有其它文件或文件夹的情况

    for dirPath, dirNames, fileNames in os.walk(path):
        for file in fileNames:
            if aID in file and file.split('.')[-1] in fileTypeList:  #
                oldName = os.path.join(dirPath, file)  # 文件全名
                if os.path.isdir(oldName):
                    continue
                fileList.append(oldName)

    fileList.sort(key=GetSeries)
    # fileList = set(fileList)  # 防止文件重复

    for oldDir in fileList:
        filetype = '.' + oldDir.split('.')[-1]
        index = int(oldDir.split('_')[-2]) - 1
        newDir = os.path.join(path, str(index + 1) + '. ' + lines[index].strip('\n') + filetype)  # 新的文件路径
        os.rename(oldDir, newDir)  # 重命名


def GetInfoList(path, aID):
    fileTypeList = aID + '.info'
    fileList = []  # 含路径的文件名

    for dirPath, dirNames, fileNames in os.walk(path):
        for file in fileNames:
            if file == fileTypeList:
                file_fullname = os.path.join(dirPath, file)  # 文件名
                fileList.append(file_fullname)
    fileList.sort(key=GetFileSeries)  # 这里必须排序
    return fileList


def GetLocalVideoTitle(path, aID):
    fileList = GetInfoList(path, aID)
    # 　print(fileList)
    titleList = []
    findVideoTitle = re.compile(r'"PartName":"(.*?)"')
    for infoFile in fileList:
        with open(infoFile, encoding='UTF-8') as f:
            lines = f.readlines()
            s = str(lines[0])
            videoTitle = re.findall(findVideoTitle, s)[0]
            titleList.append(videoTitle)
    return titleList


def GetTxt(dataList, localTitle, path):
    fileTitle = localTitle + ".txt"  # 合成.txt格式 文件名
    fileTitle = os.path.join(path, fileTitle)
    nameFile = open(fileTitle, "w", encoding="utf-8")  # 写入文件
    j = 0
    for item in dataList:
        j += 1
        nameFile.write(item + "\n")
    nameFile.close()
    return fileTitle


def DeleteTxt(delDir, delName):
    delList = os.listdir(delDir)
    for f in delList:
        if os.path.join(delDir, f) == delName:
            filePath = os.path.join(delDir, f)
            if os.path.isfile(filePath):
                os.remove(filePath)


def DeleteDir(delDir):
    # 文件夹 带 - 的会删不掉，但是文件还是删的掉的
    os.system(f"attrib -r {delDir}")  # 增加可对文件夹产生修改的权限
    shutil.rmtree(delDir, True)


# 在指定的输出文件夹下面创建名称为name的文件夹
def MakeDir(path, name):
    dir = os.path.join(path, name)

    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        dir = os.path.join(path, name + str(random.randint(0, 100)))
        os.makedirs(dir)

    return dir

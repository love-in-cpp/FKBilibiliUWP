# -*- coding = utf-8 -*-
# @Time : 2022/6/22 12:29
# @Author : 刘正阳
# @File : FileOperator.py
# @Software : PyCharm
import os
import random
import re
import shutil
import stat

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


def FindSpecialMp4Files(path, aID):
    # 提取出含有指定特征的fileList
    fileTypeList = ['mp4', 'MP4', 'mP4', 'Mp4']
    fileList = []  # 存储要copy的文件全名
    fileNameList = []
    # 获取要被命名的文件，包含了文件夹有其它文件或文件夹的情况
    for dirPath, dirNames, fileNames in os.walk(path):
        for file in fileNames:
            if aID in file and file.split('.')[-1] in fileTypeList:  #
                oldName = os.path.join(dirPath, file)  # 文件全名
                if os.path.isdir(oldName):
                    continue
                fileList.append(oldName)
                fileNameList.append(file)

    return [fileList, fileNameList]


# 检测文件是否加密 是则解密
def DecryptMp4(path, aID):
    isEncrypted = None
    s = None
    encryptedFile = None
    decryptedFile = None
    countEncChar = 0  # 检测'xff'数量
    countDecChar = 0  # 检测'x00'数量

    fileList = FindSpecialMp4Files(path, aID)[0]

    testFile = fileList[0]
    with open(testFile, "rb") as f:
        s = str(f.readline())[3:14]
    f.close()
    sList = s.split('\\')  # ['xff', 'xff', 'xff']
    for item in sList:
        if 'xff' in item:
            countEncChar += 1
        if 'x00' in item:
            countDecChar += 1

    if countEncChar == 3:
        isEncrypted = True  # 加密
    if countDecChar == 3:
        isEncrypted = False  # 未加密

    if isEncrypted is None:
        return

    if not isEncrypted:  # 如果未加密
        pass
    else:  # 如果加密则解密
        for file in fileList:
            encryptedFile = open(file, 'rb')
            encryptedFile.seek(3)
            byte = encryptedFile.read()

            with open(file, 'wb') as decryptedFile:
                decryptedFile.write(byte)

        encryptedFile.close()
        decryptedFile.close()


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


def DoRename(path, fileName, aID, isLocalPattern):
    # 获取.txt文件名
    filName = fileName
    # 读取.txt文件
    with open(filName, encoding='UTF-8') as f:
        lines = f.readlines()  # 新文件名按行保存

    fileList = FindSpecialMp4Files(path, aID)[0]  # 存储要copy的文件全名

    fileList.sort(key=GetSeries)
    # fileList = set(fileList)  # 防止文件重复
    index = 0
    frontIndex = 0
    for oldDir in fileList:
        filetype = '.' + oldDir.split('.')[-1]
        frontIndex = int(oldDir.split('_')[-2])
        if isLocalPattern:
            newDir = os.path.join(path, str(frontIndex) + '. ' + lines[index].strip('\n') + filetype)  # 新的文件路径
            index += 1
        else:
            newDir = os.path.join(path, str(frontIndex) + '. ' + lines[frontIndex-1].strip('\n') + filetype)  # 新的文件路径

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
    #　os.system(f"attrib -r {delDir}")  # 增加可对文件夹产生修改的权限
    # shutil.rmtree(delDir, True)
    if os.path.exists(delDir):
        shutil.rmtree(delDir, onerror=readonly_handler)


def readonly_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# 在指定的输出文件夹下面创建名称为name的文件夹
def MakeDir(path, name):
    dir = os.path.join(path, name)

    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        dir = os.path.join(path, name + str(random.randint(0, 100)))
        os.makedirs(dir)

    return dir


'''
FileOperator 新增
'''


# 创建记忆文件
def SaveForOutput(path, fileName):
    # fileName = "localPath.config"
    file = None
    fullpath = os.path.join(path, fileName)
    if not os.path.exists(fullpath):  # 如果路径不存在，创建路径，写入文件，返回False
        try:
            file = open(fileName, "w", encoding="utf-8")
        except:
            return
        finally:
            if file:
                file.close()
        return False
    else:
        return True


# 读文件的内容 这里的path是已经join过的
def ReadForOutput(path):
    lines = ['', '']
    if os.path.isfile(path):
        with open(path, encoding='UTF-8') as f:
            lines = f.readlines()  # 新文件名按行保存
            f.close()
    return lines


# 写入首行的内容
def WriteForOutput(path, downloadPath, outputPath):
    f = None
    try:
        f = open(path, "w", encoding="utf-8")
        f.write(downloadPath + '\n')
        f.write(outputPath)
    except:
        return
    finally:
        if f:
            f.close()
    # with open(path, "w", encoding="utf-8") as f:
    #     f.write(downloadPath+'\n')
    #     f.write(outputPath)


import base64
import datetime
import os
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import FileOperator
import TestFileSystem
from MainWindow import Ui_MainWindow
from icon import img
import TitleSpider


def GetSeries(dataList):
    return int(dataList.split('_')[1])


class MainApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.SetBaseInfo()
        self.InitMenuBar()
        self.HandleButtons()
        self.SetUI()
        self.setFixedSize(self.width(), self.height())
        self.SetLogText()
        self.progressBar.setValue(0)
        self.InitCheckBox()
        self.path = os.getcwd()
        self.saveName = "set.ini"
        self.joinedPath = os.path.join(self.path, self.saveName)  # 配置文件的位置
        self.isTextFileExists = False
        self.isTextFirstColumnHaveContent = False
        self.isTextSecondColumnHaveContent = False
        self.InitOutPutPath() # 发布绿色版时注释

    def InitOutPutPath(self):
        self.isTextFileExists = FileOperator.SaveForOutput(self.path, self.saveName)
        if self.isTextFileExists is False:  # 如果没有文件，在已经创建文件的前提下，等待用户输入手动填入OutputText. 相关事件在button事件实现
            # line = FileOperator.ReadForOutput() #
            pass
        else:  # 存在文件 则读取文件,并自动赋给文本框
            self.lines = FileOperator.ReadForOutput(self.joinedPath)
            if len(self.lines) >= 2:
                if self.lines[0] != '':
                    if os.path.isdir(self.lines[0].strip()):
                        self.downloadDirEdit.setText(self.lines[0])
                        self.isTextFirstColumnHaveContent = True
                if self.lines[1] != '':
                    if os.path.isdir(self.lines[1].strip()):
                        self.outputDirEdit.setText(self.lines[1])
                        self.isTextSecondColumnHaveContent = True

            else:
                pass
                # self.Log("检测到配置文件set.ini 为空")
                # QMessageBox.critical(self, "错误", "配置文件set.ini ！")

    def InitCheckBox(self):
        # self.txtFileCheckBox.setChecked(True)  # 默认保存Txt
        # self.deleteFileCheckBox.setChecked(False)  # 默认保留源目录
        # self.copyToOutput.setChecked(True)  # 默认使用复制的方式
        self.txtFileCheckBox.setChecked(False)  # 默认不保存Txt
        self.deleteFileCheckBox.setChecked(True)  # 默认不保留源目录
        self.moveToOutput.setChecked(True)  # 默认不使用复制的方式
        self.localMode.setChecked(True)

    def MutiThreadCopy(self, mp4List, outputPath):
        t = threading.Thread(target=FileOperator.CopyFile, args=(mp4List, outputPath))
        t.start()
        t.join()

    def MutiThreadMove(self, mp4List, outputPath):
        t = threading.Thread(target=FileOperator.MoveFile, args=(mp4List, outputPath))
        t.start()
        t.join()

    def CheckIsChecked(self):  # 按下按钮的事件里调用，检查checkbox状态，并提示。最后给对应的bool变量赋值
        self.isSaveTxt = self.txtFileCheckBox.isChecked()
        self.isDeleteDir = self.deleteFileCheckBox.isChecked()

        if self.copyToOutput.isChecked() or self.moveToOutput.isChecked():
            pass
        else:
            QMessageBox.critical(self, "错误", "请至少勾选一种输出方式！")

        if self.localMode.isChecked() or self.spiderMode.isChecked():
            pass
        else:
            QMessageBox.critical(self, "错误", "请至少勾选一种处理模式（本地模式 或 爬虫模式）！")

        if self.copyToOutput.isChecked():
            self.isCopyOutput = True
        else:
            self.isCopyOutput = False

        if self.moveToOutput.isChecked():
            self.isMoveOutput = True
        else:
            self.isMoveOutput = False

        if self.localMode.isChecked():
            self.isLocalMode = True
        else:
            self.isLocalMode = False

        if self.spiderMode.isChecked():
            QMessageBox.warning(self, "警告", "爬虫模式依赖网络，关闭本窗口前请确保代理服务是关闭状态")
            self.isSpiderMode = True
        else:
            self.isSpiderMode = False

    def SetLogText(self):
        self.activityLogEdit.setReadOnly(True)

    def Log(self, msg):
        self.statusbar.showMessage(msg)
        self.activityLogEdit.appendPlainText('[{0}]'.format(str(datetime.datetime.now())[0:19]))
        self.activityLogEdit.appendPlainText(msg)
        self.activityLogEdit.appendPlainText('')

    def LogOnBar(self, msg):
        self.statusbar.showMessage(msg)

    def HandleButtons(self):
        self.downloadDirButton.clicked.connect(self.OpenDownloadDir)
        self.outputDirButton.clicked.connect(self.OpenOutputDir)
        self.renameButton.clicked.connect(self.RenameFile)

        self.copyToOutput.clicked.connect(self.DisableMove)
        self.moveToOutput.clicked.connect(self.DisableCopy)
        self.localMode.clicked.connect(self.DisableSpiderMode)
        self.spiderMode.clicked.connect(self.DisableLocalMode)

    # 处理checkbox冲突
    def DisableCopy(self):
        if self.copyToOutput.isChecked():
            self.copyToOutput.setChecked(False)

    def DisableMove(self):
        if self.moveToOutput.isChecked():
            self.moveToOutput.setChecked(False)

    def DisableSpiderMode(self):
        if self.spiderMode.isChecked():
            self.spiderMode.setChecked(False)
        self.renameButton.setText("一键解密+整理+重命名")

    def DisableLocalMode(self):
        if self.localMode.isChecked():
            self.localMode.setChecked(False)
        self.renameButton.setText("一键解密+爬取+整理+重命名")

    def InitMenuBar(self):
        # 添加menu“帮助”的事件
        aboutAction = QAction('&关于', self)
        # aboutAction.setStatusTip('关于')
        aboutAction.triggered.connect(self.ShowAboutDialog)

        # 已有菜单栏，此处只需要添加菜单
        mainPageMenu = self.menubar.addMenu('&主页')
        helpMenu = self.menubar.addMenu('&帮助')

        # 菜单绑定之前添加的事件
        helpMenu.addAction(aboutAction)

    # 设置UI
    def SetUI(self):
        tmp = open('tmp.png', "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        icon = QIcon('tmp.png')
        os.remove("tmp.png")
        self.setWindowIcon(icon)

    def ShowAboutDialog(self):
        about_text = "<p>描述：这是一款致力于解决BiliBili UWP版下载后的视频加密、命名信息丢失和存放位置不合理等痛点的软件</p><p>版本：4.0</p><p>@Author：LZY</p><p>@github：love" \
                     "-in-cpp</p> "
        QMessageBox.about(self, '说明', about_text)

    def OpenDownloadDir(self):
        if self.isTextFirstColumnHaveContent is False:
            dName = QFileDialog.getExistingDirectory(self, '选择下载文件夹', '/')
            self.downloadDirEdit.setText(dName)
        else:
            dName = QFileDialog.getExistingDirectory(self, '选择下载文件夹', self.lines[0].strip())
            self.downloadDirEdit.setText(dName)

    def OpenOutputDir(self):
        if self.isTextSecondColumnHaveContent is False:
            dName = QFileDialog.getExistingDirectory(self, '选择输出文件夹', '/')
            self.outputDirEdit.setText(dName)
        else:
            dName = QFileDialog.getExistingDirectory(self, '选择输出文件夹', self.lines[1].strip())
            self.outputDirEdit.setText(dName)

    def SetBaseInfo(self):
        self.setWindowTitle('BiliBili UWP版视频下载整理工具')
        self.downloadDirEdit.setToolTip(r"例如：E:\BiliDownload\44938322")
        self.downloadDirEdit.setPlaceholderText("路径请具体到单个数字名称的文件夹，暂不支持文件夹的批量处理")
        self.outputDirEdit.setPlaceholderText("您希望处理后的文件被保存到的地方")

    # def FindFiles(self,downloadPath):

    def RenameFile(self):
        self.CheckIsChecked()
        self.progressBar.setValue(0)
        # 进入目录查找dvi文件
        downloadPath = self.downloadDirEdit.toPlainText()
        outputPath = self.outputDirEdit.toPlainText()
        if os.path.isdir(downloadPath) is False or os.path.isdir(self.downloadDirEdit.toPlainText().strip()) is False:
            self.Log('UWP下载目录的路径存在非法输入！')

        else:
            self.Log("进入目录：{0}".format(downloadPath))
            dviInfoList = FileOperator.GetDviInfo(downloadPath)  # 获取dvi文件信息
            if dviInfoList[0] is False:
                self.Log('没有找到.dvi文件！请检查下载目录后重试！')

            else:
                # 在outputDir下新建名为dvi[3]文件夹
                try:
                    outputPath = FileOperator.MakeDir(outputPath, dviInfoList[3])
                except Exception as e:
                    QMessageBox.critical(self, "错误", "已经存在同名文件夹！ Error：" + str(e))

                if self.isSpiderMode:
                    self.Log("开始爬取BV:{0}, 标题:{1} 的所有视频标题,请稍后...".format(dviInfoList[1], dviInfoList[3]))
                    try:
                        TitleSpider.GetTxt(dviInfoList[1], outputPath)
                    except Exception as e:
                        QMessageBox.critical(self, "错误", "请检查网络后重试 Error：" + str(e))
                    # 调用爬虫产生.txt
                    global fileName
                    fileName = TitleSpider.fileName
                    self.LogOnBar('已成功爬取文件:  {0} ！  注：只显示部分文件名'.format(fileName[0:35]))
                    self.Log('已成功爬取文件:  {0} ！'.format(fileName))

                elif self.isLocalMode:
                    self.Log("开始遍历获取BV:{0}, 标题:{1} 的所有视频标题,请稍后...".format(dviInfoList[1], dviInfoList[3]))
                    localVideoTitleList = FileOperator.GetLocalVideoTitle(downloadPath, dviInfoList[2])
                    fileName = FileOperator.GetTxt(localVideoTitleList, dviInfoList[3], outputPath)
                    self.Log('已成功获取文件:  {0} ！'.format(fileName))
                else:
                    self.Log("impossible")

                # 找到所有downloadPath的.mp4文件
                mp4List = FileOperator.FindAllMp4Files(downloadPath)[0]  # mp4真正在的地方
                # Log
                mp4nameList = FileOperator.FindAllMp4Files(downloadPath)[1]
                mp4nameList.sort(key=GetSeries)
                s = "查询到以下mp4文件：\n"
                for item in mp4nameList:
                    s += (item + '\n')
                self.Log(s)

                if os.path.isdir(outputPath) is False or os.path.isdir(self.outputDirEdit.toPlainText().strip()) is False:
                    self.Log('输出目录的路径存在非法输入！')
                else:
                    # 记忆输出目录
                    FileOperator.WriteForOutput(self.joinedPath, os.path.dirname(downloadPath), self.outputDirEdit.toPlainText()) # 发布绿色版时注释
                    # 解密
                    self.Log("开始解密...")
                    FileOperator.DecryptMp4(downloadPath, dviInfoList[2])
                    self.Log("解密完毕！")
                    # 复制
                    self.CopyOrMove(self.isCopyOutput, mp4List, outputPath)

                    # 重命名
                    self.Log("开始重命名...")
                    FileOperator.DoRename(outputPath, fileName, dviInfoList[2])
                    self.Log("重命名完毕！")

                    # 进度条100％
                    self.progressBar.setValue(100)
                    # 是否保存.txt文件
                    if self.isSaveTxt is True:
                        pass
                    else:
                        self.Log("正在删除程序运行过程中产生的.txt文件")
                        FileOperator.DeleteTxt(outputPath, fileName)
                        self.Log("删除.txt文件成功！")
                    # 是否删除源文件夹
                    if self.isDeleteDir is True:
                        self.Log("正在删除源文件夹")
                        FileOperator.DeleteDir(downloadPath)
                        self.Log("删除源文件夹成功！")
                    else:
                        pass
                    # 重命名输出文件夹 搁置

    # 输出方式：复制或移动
    def CopyOrMove(self, isCopyTo, mp4List, outputPath):
        if isCopyTo is True:
            self.Log("进入目录：{0}".format(outputPath))
            self.Log("开始复制... 这可能需要一段时间...")
            self.MutiThreadCopy(mp4List, outputPath)  # 多线程复制
            self.Log("复制完毕！")
        else:
            self.Log("进入目录：{0}".format(outputPath))
            self.Log("开始移动... 这可能需要一段时间...")
            self.MutiThreadMove(mp4List, outputPath)  # 多线程移动
            self.Log("移动完毕！")

    def DSpiderMode(self):
        pass

    def DoLocalMode(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()

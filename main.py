import base64
import datetime
import os
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import FileOperator
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

    def InitCheckBox(self):
        # self.txtFileCheckBox.setChecked(True)  # 默认保存Txt
        # self.deleteFileCheckBox.setChecked(False)  # 默认保留源目录
        # self.copyToOutput.setChecked(True)  # 默认使用复制的方式
        self.txtFileCheckBox.setChecked(False)  # 默认不保存Txt
        self.deleteFileCheckBox.setChecked(True)  # 默认不保留源目录
        self.moveToOutput.setChecked(True)  # 默认不使用复制的方式

    def MutiThreadCopy(self, mp4List, outputPath):
        t = threading.Thread(target=FileOperator.CopyFile, args=(mp4List, outputPath))
        t.start()
        t.join()

    def MutiThreadMove(self, mp4List, outputPath):
        t = threading.Thread(target=FileOperator.MoveFile, args=(mp4List, outputPath))
        t.start()
        t.join()

    def CheckIsChecked(self):
        self.isSaveTxt = self.txtFileCheckBox.isChecked()
        self.isDeleteDir = self.deleteFileCheckBox.isChecked()

        if self.copyToOutput.isChecked() or self.moveToOutput.isChecked():
            pass
        else:
            QMessageBox.critical(self, "错误", "请至少勾选一种输出方式！")

        if self.copyToOutput.isChecked():
            self.isCopyOutput = True
        else:
            self.isCopyOutput = False

        if self.moveToOutput.isChecked():
            self.isMoveOutput = True
        else:
            self.isMoveOutput = False

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

    def DisableCopy(self):
        if self.copyToOutput.isChecked():
            self.copyToOutput.setChecked(False)

    def DisableMove(self):
        if self.moveToOutput.isChecked():
            self.moveToOutput.setChecked(False)

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
        about_text = "<p>描述：这是一个致力于解决BiliBiLi UWP版下载视频的名称十分反人类的痛点的软件</p><p>版本：1.0</p><p>@Author：LZY</p><p>@github：love" \
                     "-in-cpp</p> "
        QMessageBox.about(self, '说明', about_text)

    def OpenDownloadDir(self):
        dName = QFileDialog.getExistingDirectory(self, '选择文件夹', '/')
        self.downloadDirEdit.setText(dName)

    def OpenOutputDir(self):
        dName = QFileDialog.getExistingDirectory(self, '选择文件夹', '/')
        self.outputDirEdit.setText(dName)

    def SetBaseInfo(self):
        self.setWindowTitle('BiliBili UWP版视频下载整理工具')
        self.downloadDirEdit.setToolTip(r"例如：E:\BiliDownload\44938322")
        self.downloadDirEdit.setPlaceholderText("路径请具体到下载的视频对应的单个文件夹，暂不支持批量处理")
        self.outputDirEdit.setPlaceholderText("您希望处理后的文件被保存到的地方")

    # def FindFiles(self,downloadPath):

    def RenameFile(self):
        self.CheckIsChecked()
        # 进入目录查找dvi文件
        downloadPath = self.downloadDirEdit.toPlainText()

        if os.path.isdir(downloadPath) is False:
            self.Log('UWP下载目录的路径存在非法输入！')

        else:
            self.Log("进入目录：{0}".format(downloadPath))
            dviInfoList = FileOperator.GetDviInfo(downloadPath)  # 获取dvi文件信息
            if dviInfoList[0] is False:
                self.Log('没有找到.dvi文件！请检查下载目录后重试！')

            else:

                self.Log("开始爬取BV:{0}, 标题:{1} 的所有视频标题,请稍后...".format(dviInfoList[1], dviInfoList[3]))
                TitleSpider.GetTxt(dviInfoList[1])  # 调用爬虫
                global fileName
                fileName = TitleSpider.fileName
                self.LogOnBar('已成功爬取文件:  {0} ！  注：只显示部分文件名'.format(fileName[0:35]))
                self.Log('已成功爬取文件:  {0} ！'.format(fileName))

                # 找到所有downloadPath的.mp4文件
                mp4List = FileOperator.FindAllMp4Files(downloadPath)[0]  # mp4真正在的地方

                # Log
                mp4nameList = FileOperator.FindAllMp4Files(downloadPath)[1]
                mp4nameList.sort(key=GetSeries)
                s = "查询到以下mp4文件：\n"
                for item in mp4nameList:
                    s += (item + '\n')
                self.Log(s)

                # 复制
                outputPath = self.outputDirEdit.toPlainText()
                if os.path.isdir(outputPath) is False:
                    self.Log('输出目录的路径存在非法输入！')
                else:
                    self.CopyOrMove(self.isCopyOutput, mp4List, outputPath)

                    # 重命名
                    self.Log("开始重命名...")
                    FileOperator.DoRename(outputPath, fileName)
                    self.Log("重命名完毕！")

                    # 进度条100％
                    self.progressBar.setValue(100)
                    # 是否保存.txt文件
                    if self.isSaveTxt is True:
                        pass
                    else:
                        self.Log("正在删除程序运行过程中产生的.txt文件")
                        FileOperator.DeleteTxt(os.getcwd(), fileName)
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


if __name__ == '__main__':
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec_()

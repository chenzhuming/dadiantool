import sys
import os
from ConfigIni import ConfigIni
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import threading
import time
import subprocess
import re
import json
from PyQt5 import QtGui
'''
控制台输出定向到Qtextedit中
'''


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()  # Custom output stream.
        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def initUI(self):
        global logcat_flag
        logcat_flag = 0
        global log_name
        log_name = ''
        global dadiantype
        dadiantype = 0
        # 读取配置文件
        global regs
        regs = []
        self.ConfigIni = ConfigIni("config.ini")
        regs.append(self.ConfigIni.read("reg", "keyword"))
        regs.append(self.ConfigIni.read("reg", "interface"))
        regs.append(self.ConfigIni.read("reg", "custom"))
        # self.grid = QGridLayout()
        self.grid = QGridLayout()
        self.deviceIp = QLabel('IP：')
        self.Edit_deviceIp = QLineEdit()
        self.Edit_deviceIp.setInputMask('000.000.000.000; ')
        self.Edit_deviceIp.setText('192.168')
        self.btn_deviceIp = QPushButton('连接设备')
        self.btn_disConnect = QPushButton('断开设备')
        self.btn_devices = QPushButton('查看设备')
        self.btn_logcat = QPushButton('开始打点')
        self.btn_clear = QPushButton('清空')
        self.process = QTextEdit(self, readOnly=True)

        self.combo = QComboBox(self)
        self.combo.addItem("关键字")
        self.combo.addItem("接口名")
        self.combo.addItem("自定义正则表达式")
        self.edit_regText = QLineEdit(regs[0])

        self.btn_save = QPushButton('保存')
        self.grid.addWidget(self.deviceIp, 1, 0)
        self.grid.addWidget(self.Edit_deviceIp, 1, 1)
        self.grid.addWidget(self.btn_deviceIp, 1, 2)
        self.grid.addWidget(self.btn_disConnect, 1, 3)
        self.grid.addWidget(self.btn_devices, 1, 4)
        self.grid.addWidget(self.btn_logcat, 1, 5)
        self.grid.addWidget(self.btn_clear, 1, 6)
        self.grid.addWidget(self.combo, 2, 0)
        self.grid.addWidget(self.edit_regText, 2, 1)
        self.grid.addWidget(self.btn_save, 2, 2)

        self.grid.addWidget(self.process, 3, 0, 1, 7)
        self.btn_deviceIp.clicked.connect(self.deviceConnect)
        self.btn_disConnect.clicked.connect(self.deviceDisConnect)
        self.btn_devices.clicked.connect(self.QueryingDevices)
        self.btn_logcat.clicked.connect(self.logcat)
        self.btn_clear.clicked.connect(self.clearMethod)
        self.btn_save.clicked.connect(self.saveReg)
        self.combo.activated[str].connect(self.onActivated)
        font = QtGui.QFont()
        font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font.setPointSize(18)  # 括号里的数字可以设置成自己想要的字体大小
        self.process.setFont(font)
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 600, 450)
        self.move(300, 150)
        self.setWindowTitle('打点工具')
        self.showMaximized()
        self.show()

    def onActivated(self, text):
        global dadiantype
        global regs
        if text == "关键字":
            self.edit_regText.setText(regs[0])
            dadiantype = 0
        elif text == "接口名":
            self.edit_regText.setText(regs[1])
            dadiantype = 1
        else:
            self.edit_regText.setText(regs[2])
            dadiantype = 2

    def adb(self, n, m=''):
        t = threading.Thread(target=self.run, args=(n, m))
        t.start()

    def run(self, pi, pm):
        print(time.strftime('%Y-%m-%d %H:%M:%S',
                            time.localtime(time.time())) + ' >>> '+pi+pm)
        p = subprocess.Popen(pi, shell=True, stdout=subprocess.PIPE)
        p1 = p.stdout.read()
        print(str(p1, 'utf-8'))
        # p.kill()

    def deviceConnect(self):
        ip = self.Edit_deviceIp.text()
        self.adb('adb connect ' + ip)

    def deviceDisConnect(self):
        ip = self.Edit_deviceIp.text()
        self.adb('adb disconnect ' + ip)

    def QueryingDevices(self):
        self.adb('adb devices')

    def logcat(self):
        global logcat_flag
        if logcat_flag == 0:
            path = ('./log')
            if not os.path.exists(path):
                os.mkdir(path)
            # print(path)
            now = time.strftime('%Y-%m-%d-%H-%M-%S')
            global log_name
            log_name = now+'.log'
            self.adb('adb logcat -c')
            self.adb('adb logcat >'+'"'+path+'/'+now+'.log"',
                     '\n正在打点......\n如完成，请按“分析打点”按钮停止！')
            # print('adb logcat >'+'"'+path+'//'+now+'.log"')
            self.btn_logcat.setText('分析打点')
            logcat_flag = 1
        else:
            self.Logcat_stop()

    def Logcat_stop(self):
        t = threading.Thread(target=self.run_logcat_stop, args=())
        t.start()

    def run_logcat_stop(self):
        match = 'a'
        while match != None:
            pi = 'adb shell "ps | grep logcat"'
            # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' >>> ' + pi)
            # print('\n')
            p = subprocess.Popen(pi, shell=True, stdout=subprocess.PIPE)
            p1 = p.stdout.read()
            print(str(p1, 'utf-8'))
            match = re.search(r'\d+', str(p1, 'utf-8')[10:])
            if match:
                pid_logcat = match.group(0)
                self.adb('adb shell kill -9 '+pid_logcat+'\n')
        global logcat_flag
        logcat_flag = 0
        print('已完成打点！')
        self.btn_logcat.setText('开始打点')
        global dadiantype
        # 将三种分析提取成一个方法
        self.analysis(self.edit_regText.text(), dadiantype)
        # if dadiantype == 0:
        #     self.fenxi(self.edit_regText.text())
        # elif dadiantype == 1:
        #     self.fenxiinterface(self.edit_regText.text())
        # else:
        #     self.fenxireg(self.edit_regText.text())

    def clearMethod(self):
        self.process.setText("")
    # 保存配置文件
    def saveReg(self):
        global dadiantype
        global regs
        regs[dadiantype]=self.edit_regText.text()
        if dadiantype == 0:
            self.ConfigIni.update("reg", "keyword", self.edit_regText.text())
        elif dadiantype == 1:
            self.ConfigIni.update("reg", "interface", self.edit_regText.text())
        else:
            self.ConfigIni.update("reg", "custom", self.edit_regText.text())
        print("保存成功")

    def analysis(self, text, dadiantype):
        # print("接口打点")
        global log_name
        if log_name == '':
            return
        f = open("./log/"+log_name, 'r', encoding='UTF-8', errors='ignore')
        lines = f.readlines()
        flines = len(lines)
        content = []
        print("dadiantype==%s,text:%s" % (dadiantype, text))
        # 关键字打点
        if dadiantype == 0:
            regex = re.compile(text+r'\-{3}(.*?)\]')
        # 接口名打点
        elif dadiantype == 1:
            regex = re.compile(r'requestBody is\s*(.*?)\]')
        # 自定义正则打点
        else:
            regex = re.compile(text)
        # 逐行匹配数据.
        for i in range(flines):
            # if text not in lines[i]:
            #     continue
            match = regex.search(lines[i])
            if match is not None:
                print('----------------------')
                a = json.loads(match.group(1))
                print(json.dumps(a, sort_keys=True, indent=4, ensure_ascii=False))

    def fenxi(self, text):
        # print("关键字打点")
        global log_name
        if log_name == '':
            return
        # f = open("./log/"+"2020-08-27-12-22-01.log",'r', encoding='UTF-8')
        f = open("./log/"+log_name, 'r', encoding='UTF-8')
        lines = f.readlines()
        flines = len(lines)
        content = []
        # regex = re.compile(r'\[requestbody\s*is\s*(.*?)\]'))
        regex = re.compile(text+r'\-{3}(.*?)\]')
        # 逐行匹配数据.
        for i in range(flines):
            match = regex.search(lines[i])
            if match is not None:
                print('----------------------')
                a = json.loads(match.group(1))
                print(json.dumps(a, sort_keys=True, indent=4, ensure_ascii=False))

    def fenxiinterface(self, text):
        # print("接口打点")
        global log_name
        if log_name == '':
            return
        # f = open("./log/"+"145224.txt",'r', encoding='UTF-8',errors='ignore')
        f = open("./log/"+log_name, 'r', encoding='UTF-8', errors='ignore')
        lines = f.readlines()
        flines = len(lines)
        content = []
        # regex = re.compile(r'\[requestbody\s*is\s*(.*?)\]'))
        regex = re.compile(r'requestBody is\s*(.*?)\]')
        # 逐行匹配数据.
        for i in range(flines):
            if text not in lines[i]:
                continue
            match = regex.search(lines[i])
            if match is not None:
                print('----------------------')
                a = json.loads(match.group(1))
                print(json.dumps(a, sort_keys=True, indent=4, ensure_ascii=False))

        def fenxireg(self, text):
            # print("自定义正则打点")
            global log_name
            if log_name == '':
                return
            # f = open("./log/"+"145224.txt",'r', encoding='UTF-8',errors='ignore')
            f = open("./log/"+log_name, 'r', encoding='UTF-8', errors='ignore')
            lines = f.readlines()
            flines = len(lines)
            content = []
            # regex = re.compile(r'\[requestbody\s*is\s*(.*?)\]'))
            regex = re.compile(text)
            # 逐行匹配数据.
            for i in range(flines):
                if text not in lines[i]:
                    continue
                match = regex.search(lines[i])
                if match is not None:
                    print('----------------------')
                    a = json.loads(match.group(1))
                    print(json.dumps(a, sort_keys=True,
                                     indent=4, ensure_ascii=False))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

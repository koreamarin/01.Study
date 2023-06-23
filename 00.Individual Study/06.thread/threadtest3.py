# https://www.youtube.com/watch?v=3ogKXcmZncc
import sys, time, threading, time, random, os
from PyQt5.QtWidgets import *
from PyQt5 import uic

s = threading.Semaphore(10)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "threadtest3.ui"

class thr(threading.Thread) :
    def  __init__(self, pBar):
        super().__init__()
        self.pBar = pBar

    def run(self) :
        s.acquire()
        for v in range(1, 101) :
            self.pBar.setValue(v)
            time.sleep(0.001)
        s.release()

class MainDialog(QDialog) :
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)

        self.lst = []                       # 프로그래스 바를 담을 리스트
        self.lstThr = []                    # 쓰레스 객체를 담을 리스트
        self.vBox = QVBoxLayout(self)       # 세로로 쌓는 VBoxLayout
        self.hBox = QHBoxLayout(self)       # 가로로 쌓는 HBoxLayout

        self.lst.append(self.progressBar_1)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_2)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_3)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_4)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_5)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_6)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_7)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_8)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_9)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.
        self.lst.append(self.progressBar_10)     # ProgressBar 10개를 생성하고, 리스트에 그 ProgressBar를 추가함.

        for i in range(10) :                        # 10개의 프로그래스바와 그 리스트를 생성하고 vBox에 담는 반복문.
            self.vBox.addWidget(self.lst[i])        # vbox Layout에도 ProgressBar가 담긴 리스트를 추가함.

        self.btn1.clicked.connect(self.normal)      # btn1 버튼에 클릭동작으로 보통 진행 함수추가.
        self.btn2.clicked.connect(self.thrMode)     # btn2 버튼에 클릭동작으로 쓰레드 진행 함수추가.
        self.btn3.clicked.connect(self.reset)       # btn3 버튼에 클릭동작으로 리셋 함수추가.

    def normal(self) :
        for i in range(10) :
            for v in range(101) :
                self.lst[i].setValue(v)
                time.sleep(0.001)
    
    def thrMode(self) :
        for i in range(10) :
            self.lstThr.append(thr(self.lst[i]))
            self.lstThr[-1].start()
        for k in self.lstThr:
            k.join()
        
    def reset(self) :
        for i in range(10) :
            self.lst[i].setValue(0)

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
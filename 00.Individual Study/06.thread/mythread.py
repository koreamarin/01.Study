# https://www.youtube.com/watch?v=3ogKXcmZncc
import sys, time, threading, time, os
from PyQt5.QtWidgets import *
from PyQt5 import uic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "mythread.ui"

class MainDialog(QDialog) :
    exit = []
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)

        self.btn2.clicked.connect(self.thrMode)             # btn2 버튼에 클릭동작으로 쓰레드 진행 함수추가.
        self.btn3.clicked.connect(self.auto_thrMode)        # btn3 버튼에 클릭동작으로 리셋 함수추가.
        self.btn4.clicked.connect(self.exit)                # btn3 버튼에 클릭동작으로 리셋 함수추가.

    
    def thrMode(self) :
        t1 = threading.Thread(target=self.run)
        t1.daemon=True
        t1.start()
        
    def auto_thrMode(self) :
        if self.btn3.text() == '자동 스레드 시작' :
            self.btn3.setText('자동 스레드 중지')
            self.exit = False
            t2 = threading.Thread(target=self.auto_run)
            t2.daemon=True
            t2.start()
        elif self.btn3.text() == '자동 스레드 중지' :
            self.btn3.setText('자동 스레드 시작')
            self.exit = True

    def auto_run(self) :
        while True :
            if self.exit == True :
                print('Infinite Loop Stop!')
                return
            self.run()
            time.sleep(int(self.spinBox.text()))

    def run(self) :
        for v in range(11) :
            if v == 10 :
                print(v)
            time.sleep(0.001)

    def exit(self):
        sys.exit(0)

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
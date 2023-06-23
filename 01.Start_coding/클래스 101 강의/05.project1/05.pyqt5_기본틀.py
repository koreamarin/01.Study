# 심화 - GUI 환경이란? Qt designer로 pyqt5 개발 짱쉽게 하기
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = "디자인 파일명"

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)

QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())




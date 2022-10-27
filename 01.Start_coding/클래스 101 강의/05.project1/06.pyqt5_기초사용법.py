# 심화 - GUI 환경이란? Qt designer로 pyqt5 개발 짱쉽게 하기
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

UI_PATH = r'startcoding\클래스 101 강의\05.project1\practice.ui'


class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(UI_PATH, self)

        # 1) 버튼 클릭 이벤트
        # self.객체이름.clicked.connect(self.실행할함수이름)        --> 함수뒤에 괄호안씀
        self.login_btn.clicked.connect(self.login_start)


    def login_start(self) :  
        print("로그인 버튼 클릭됨")
        # 2) 입력창 텍스트 값 추출
        # self.객체이름.text()
        input_id = self.id.text()
        input_pw = self.pw.text()
        print("아이디   : ", input_id)
        print("비밀번호 : ", input_pw)





QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())




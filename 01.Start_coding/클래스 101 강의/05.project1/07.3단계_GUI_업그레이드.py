# 심화 - 외주 프로그램처럼 GUI 환경 개발 완성하기
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import requests
import json
import os

UI_PATH = r"startcoding\클래스 101 강의\05.project1\design.ui"
sub_list = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(UI_PATH, self)
        self.search_btn.clicked.connect(self.search_start)
        self.reset.clicked.connect(self.search_reset)
        self.save_btn.clicked.connect(self.save)
        self.end_btn.clicked.connect(self.end)

    def search_start(self) :
        self.status_msg.setText("자동완성 키워드 추출을 시작합니다...")
        QApplication.processEvents()                                    # 이걸 안쓰면 자동완성 키워드 추출을 시작합니다가 뜨지 않는다. 하나의 동작이 완료되고 나서야 이벤트가 발생하는데, 이 문장을 쓰면 바로 바뀌어야할 이벤트를 발생시키는 기능을 하므로 텍스트 출력이 가능하다.
        main_keyword = self.lineEdit.text()
        for sub in sub_list :
            keyword = main_keyword + ' ' + sub
            response = requests.get(f"https://ac.search.naver.com/nx/ac?q={keyword}&con=0&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100&_callback=_jsonp_4")
            origin_data = response.text
            str_data = origin_data.split("_jsonp_4(")[1][:-1]
            dic_data = json.loads(str_data)
            for data in dic_data['items'][0] :
                self.textBrowser.append(data[0])

        self.status_msg.setText("자동완성 키워드 추출이 완료되었습니다.")

    def search_reset(self) :
        self.textBrowser.setText("")
        self.lineEdit.setText("")
        self.status_msg.setText("리셋 되었습니다.")
    
    def save(self) : 
        result = self.textBrowser.toPlainText()
        f = open(rf'C:\Users\USER\OneDrive\바탕 화면\python\startcoding\클래스 101 강의\05.project1\{self.lineEdit.text()}_연관검색어.txt', 'w', encoding='utf-8')
        f.write(result)
        f.close()
        self.status_msg.setText(os.getcwd() + f'\startcoding\클래스 101 강의\05.project1\{self.lineEdit.text()}_연관검색어.txt 에 저장 되었습니다.')        # os.getcwd() -> 현재 프로젝트의 위치를 추출

    def end(self) :
        sys.exit()


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())




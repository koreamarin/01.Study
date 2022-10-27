# 심화 - 외주 프로그램처럼 GUI 환경으로 완성해보기
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip

UI_PATH = r"startcoding\클래스 101 강의\07.project3\design.ui"

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(UI_PATH, self)

        self.start_btn.clicked.connect(self.main)
        self.slider.valueChanged.connect(self.change_slider_value)

    def change_slider_value(self) :
        self.max.setText(str(self.slider.value()))            # --> self.slider.value 값이 정수형이므로 text로 출력하기 위하여 str로 형변환

    def main(self) : 
        input_id = self.id.text()
        input_pw = self.pw.text()
        input_max = int(self.max.text())                    # --> self.max.text 값이 문자형이므로 input_max로 넣기 위하여 int(정수형)으로 형변환


        # validation check (유효성 검사)
        if input_id == "" or input_pw =="" :
            self.status.append("빈칸을 채워주세요")         # --> lable의 문자를 바꿀때에는 setText, TextBrowser의 문자를 출력할때에는 append를 쓴다.
            return 0    # 함수를 종료시킴

        self.status.append("로그인 진행중...")
        QApplication.processEvents()

        driver = self.login(input_id, input_pw)

        if driver == 0 :
            self.status.append("로그인 실패, 아이디 비밀번호 확인요망")
            return 0
        
        else :
            self.status.append("로그인 성공!")
            QApplication.processEvents()
            time.sleep(1)
            self.status.append("자동화 진행중...")
            QApplication.processEvents()
            self.start(driver, input_max)
            self.status.append("자동화 완료!")
            

    def login(self, input_id, input_pw) : 
        # 브라우저 꺼짐 방지
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # 불필요한 에러 메시지 없애기
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = Service(executable_path=ChromeDriverManager().install())  
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 웹페이지 해당 주소 이동
        driver.implicitly_wait(3)
        driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

        # 아이디 입력창
        id = driver.find_element(By.CSS_SELECTOR, "#id")
        id.click()
        pyperclip.copy(input_id)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        # 비밀번호 입력창
        pw = driver.find_element(By.CSS_SELECTOR, "#pw")
        pw.click()
        pyperclip.copy(input_pw)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        # 로그인 버튼
        login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
        login_btn.click()
        time.sleep(1)

        # 로그인 완료
        # 로그인 성공 시 드라이버 반환
        # 로그인 실패 시 드라이버 종료 후 숫자 0 반환

        check = driver.find_elements(By.CSS_SELECTOR, "#minime")

        if len(check) > 0 :
            return driver
        else :
            driver.close()
            return 0

    
    def start(self, driver,input_max) :
        # 이웃 새글 페이지 이동 (모바일)
        driver.get("http://m.blog.naver.com/FeedList.naver")

        time.sleep(2)

        n = input_max   # 총 좋아요 개수
        count = 0       # 현재 좋아요 신청 개수

        while count < n :
            btns = driver.find_elements(By.CSS_SELECTOR, ".u_likeit_list_btn._button.off")

            # 더 이상 누를 좋아요 버튼이 없다면,
            # 반복문 종료
            if len(btns) == 0 :
                break

            # 좋아요가 안눌린 첫번째 게시글 누르기
            btns[0].click()

            # 현재 좋아요 신청 개수 +1
            count = count + 1
            time.sleep(1)








QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())







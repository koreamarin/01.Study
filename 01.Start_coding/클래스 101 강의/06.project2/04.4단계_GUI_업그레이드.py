# 심화 - 외주 프로그램같이 GUI 환경으로 업그레이드해보기
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

UI_PATH = r"startcoding\클래스 101 강의\06.project2\design.ui"

class MainDialog(QDialog) :
    def __init__(self) :
        QDialog.__init__(self, None)
        uic.loadUi(UI_PATH, self)

        self.start_btn.clicked.connect(self.main)

    def main(self) : 
        input_id = self.id.text()
        input_pw = self.pw.text()
        input_keyword = self.keyword.text()
        input_max = self.max.value()
        input_message = self.message.toPlainText()

        # validation check (유효성 검사)
        if input_id == "" or input_pw =="" or input_keyword == "" or input_max == "" or input_message == "" :
            self.status.setText("빈칸을 채워주세요")
            return 0    # 함수를 종료시킴

        self.status.setText("로그인 진행중...")
        QApplication.processEvents()

        driver = self.login(input_id, input_pw)

        if driver == 0 :
            self.status.setText("로그인 실패, 아이디 비밀번호 확인요망")
            return 0
        
        else :
            self.status.setText("로그인 성공!")
            QApplication.processEvents()
            time.sleep(1)
            self.status.setText("자동화 진행중...")
            QApplication.processEvents()
            self.start(driver, input_keyword, input_max, input_message)
            self.status.setText("자동화 완료!")
            

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
        driver.maximize_window()
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

    
    def start(self, driver, input_keyword, input_max, input_message) :
        search_url = f"https://m.search.naver.com/search.naver?where=m_blog&query={input_keyword}&sm=mtb_viw.blog&nso=so%3Add%2Cp%3Aall"

        driver.get(search_url)
        time.sleep(1)

        n = input_max           # 이웃 신청 개수
        count = 0               # 현재 이웃 신청 개수
        index = 0               # 현재 블로그 글 번호

        while count < n :
            ids = driver.find_elements(By.CSS_SELECTOR, ".sub_txt.sub_name")
            
            # 블로그 아이디 클릭
            # 현재 블로그 글 번호에 맞는 아이디 찾기
            id = ids[index]

            # 새창으로 열기
            id.send_keys(Keys.CONTROL + '\n')

            # 새창으로 드라이버 전환
            all_windows = driver.window_handles
            driver.switch_to.window(all_windows[1])
            time.sleep(2)

            try:
                # 이웃 추가 버튼 클릭
                driver.find_element(By.CSS_SELECTOR, ".link__RsHMX.add_buddy_btn__oGR_B").click()

                # 서로 이웃 버튼 클릭
                driver.find_element(By.CSS_SELECTOR, "#bothBuddyRadio").click()

                textarea = driver.find_element(By.CSS_SELECTOR, ".textarea_t1")
                textarea.send_keys(Keys.CONTROL, 'a')
                time.sleep(1)
                textarea.send_keys(Keys.DELETE)
                time.sleep(1)
                textarea.send_keys(input_message)
                time.sleep(1)

                # 확인 버튼 클릭
                driver.find_element(By.CSS_SELECTOR, ".btn_ok").click()
                count = count + 1   # 현재 이웃 신청 개수 증가
            
            except :
                pass
        
            # 새창 닫기
            driver.close()

            # 기존 창으로 드라이버 전환
            driver.switch_to.window(all_windows[0])
            index = index + 1   # 현재 블로그 글 번호 증가






QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())







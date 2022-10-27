# 웹사이트 자동화 방법

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기 (꼭 필요한 코드는 아님. 없어도됨. 다만 이상한 오류코드가 발생하기에 그거 없애려고 추가하는 것)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 웹브라우저 띄우기 (크롬드라이버매니저를 통해 최신버전으로 업데이트설치하고 service라는 객체에 저장한다는 뜻.)
service = Service(executable_path=ChromeDriverManager().install())

# 셀레니움 webdriver의 Chrome으로 최신 버전인 service 객체를 가져와서 그 정보를 driver에 저장함. options에는 chrome_options를 추가하여 웹 꺼짐 방지 기능을 추가함
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.implicitly_wait(5)   # 웹페이지가 로딩 될때까지 5초는 기다림
driver.maximize_window()    # 화면 최대화

driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")        # 네이버 로그인 URL로 이동

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui        # 아직 잘 모름...핫키를 다룰 수 있는 것 같음
import pyperclip        # 클립보드 관련을 다루는 라이브러리


# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기, 부착된 장치가 작동하지 않습니다 등.....
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

#크롬드라이버매니저를 이용해서 크롬드라이버를 최신버전으로 자동으로 설치해줌
service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

# 주소 이동
driver.implicitly_wait(5)   # 웹페이지가 로딩 될때까지 5초는 기다림
driver.maximize_window()    # 화면 최대화
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

time.sleep(2)

# 아이디 입력창
id = driver.find_element(By.CSS_SELECTOR, "#id")
id.click()
# id.send_keys("awldnjs2")       # 너무 빨리 입력해서 자동로그인방지시스템에 막힘

# 복붙으로 로그인방지 뚫는 방법 --> 이 방법만 뚫림
pyperclip.copy("awldnjs2")      # 클립보드에 문자 복사
pyautogui.hotkey("ctrl","v")    # ctrl v 동시에 눌러 붙여넣기

# 느린 키보드 타이핑으로 로그인 방지 뚫는 방법  --> 안뚫리네;;
# pyautogui.write('awldnjs2', interval=0.25)

time.sleep(3)

# 비밀번호 입력창
pw = driver.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
# pw.send_keys("quality12#")     # 너무 빨리 입력해서 자동로그인방지시스템에 막힘

# 복붙으로 로그인방지 뚫는 방법 --> 이 방법만 뚫림
pyperclip.copy("quality12#")      # 클립보드에 문자 복사
pyautogui.hotkey("ctrl","v")    # ctrl v 동시에 눌러 붙여넣기

# 느린 키보드 타이핑으로 로그인 방지 뚫는 방법 --> 안뚫리네;;
# pyautogui.write('quality12#', interval=0.25)

time.sleep(3)

# 로그인 클릭
login = driver.find_element(By.CSS_SELECTOR, "#log\.login")
login.click()




# # 탭 이동
# driver.switch_to.window(driver.window_handles[1])

# # 새 탭 닫기
# driver.close()

# # 브라우저 닫기
# driver.quit()

# # iframe 안으로 들어가기
# driver.switch_to.frame("id값")  ex) driver.switch_to.frame("se2_iframe")

# # iframe 밖으로 나오기
# driver.switch_to.default_content()
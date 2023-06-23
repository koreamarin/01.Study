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

# 웹페이지가 로딩 될때까지 5초는 기다림
driver.implicitly_wait(5)
# 화면 최대화
driver.maximize_window()

# 웹페이지 해당 주소 이동
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")        # 네이버 로그인 URL로 이동

# 아이디 입력창에 아이디 입력
id = driver.find_element(By.CSS_SELECTOR, "#id")                # driver내에서 CSS 선택자 "#id"로 아이디 입력창을 찾은 후, 그 정보를 id라는 변수에 담는다.
id.click()                                                      # 찾은 아이디 입력창을 클릭
# id.send_keys("awldnjs2")                                       --> 이 방법으로 비밀번호 입력하면 봇에 막힘
pyperclip.copy('awldnjs2')                                      # 클립보드에 아이디 복사
pyautogui.hotkey('ctrl', 'v')                                   # 아이디 붙여넣기
time.sleep(1)

# 비밀번호 입력창에 비밀번호 입력
pw = driver.find_element(By.CSS_SELECTOR, "#pw")                # driver내에서 CSS 선택자 "#id"로 아이디 입력창을 찾은 후, 그 정보를 id라는 변수에 담는다.
pw.click()                                                      # 찾은 아이디 입력창을 클릭
# pw.send_keys("quality12#")                                     --> 이 방법으로 비밀번호 입력하면 봇에 막힘
pyperclip.copy('quality12#')                                    # 클립보드에 비밀번호 복사
pyautogui.hotkey('ctrl', 'v')                                   # 아이디 붙여넣기
time.sleep(1)

# 로그인 버튼 클릭
driver.find_element(By.CSS_SELECTOR, "#log\.login").click()

# 메일함으로 이동
driver.get("https://mail.naver.com/")
time.sleep(1)

# 메일쓰기 버튼 클릭
driver.find_element(By.CSS_SELECTOR, '#nav_snb > div.btn_workset > a.btn_quickwrite._c1\(mfCore\|popupWrite\|new\)._ccr\(lfw\.write\)._stopDefault > strong > span').click()
time.sleep(1)

# 받는사람 선택자에 아이디 입력
driver.find_element(By.CSS_SELECTOR, '#toInput').send_keys("qkrtpgus152@naver.com")
time.sleep(1)

# 제목
driver.find_element(By.CSS_SELECTOR, '#subject').send_keys("자동화 프로그램 연습중")
time.sleep(1)

# 본문에 들어가기 전에 iframe 안으로 들어가기
driver.switch_to.frame('se2_iframe')                # 괄호안에 ifrmae의 id 입력
time.sleep(1)

# 본문
driver.find_element(By.CSS_SELECTOR, 'body').send_keys("웹사이트 및 메일 자동화 프로그램 연습중인데 보낼사람이 없어서 보냄.")
time.sleep(1)

# iframe 밖으로 나오기
driver.switch_to.default_content()
time.sleep(1)

# 보내기 버튼 클릭
driver.find_element(By.CSS_SELECTOR, "#sendBtn").click()



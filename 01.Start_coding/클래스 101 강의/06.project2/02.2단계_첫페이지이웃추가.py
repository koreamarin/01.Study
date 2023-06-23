# 웹사이트 자동화 방법

from cgitb import text
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
# pw.send_keys("wldnjs12#")                                     --> 이 방법으로 비밀번호 입력하면 봇에 막힘
pyperclip.copy('wldnjs12#')                                    # 클립보드에 비밀번호 복사
pyautogui.hotkey('ctrl', 'v')                                   # 아이디 붙여넣기
time.sleep(1)


# 로그인 버튼 클릭
login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
login_btn.click()
time.sleep(1)

# 로그인 완료

# 키워드 : 재테크
# 정렬 : 블로그, 최신순
search_url = "https://m.search.naver.com/search.naver?where=m_blog&query=%EC%9E%AC%ED%85%8C%ED%81%AC&sm=mtb_viw.blog&nso=so%3Add%2Cp%3Aall"

driver.get(search_url)
time.sleep(1)

# 블로그 아이디 선택자
ids = driver.find_elements(By.CSS_SELECTOR, ".sub_txt.sub_name")           # 1개만 가져와야하므로 elements가 아닌 element를 씀
time.sleep(1)

for id in ids:
    # 새 탭으로 열기
    id.send_keys(Keys.CONTROL + '\n')           # ctrl 누르고 마우스 클릭하면 새 탭으로 열리는것처럼 CSS선택자를 통해 선택한 상대를 ctrl + \n 하면 새 탭으로 띄워지는 기능인 것으로 추정됨.

    # 새탭으로 드라이버 전환
    all_windows = driver.window_handles         # 드라이버가 제어하고 있는 모든 크롬 윈도우를 all_windows 변수에 넣어 
    driver.switch_to.window(all_windows[1])     # all_winddows[1]을 선택하여 2번째 탭으로 전환.
    time.sleep(1)

    try :
        # 이웃추가버튼 클릭
        driver.find_element(By.CSS_SELECTOR, ".link__RsHMX.add_buddy_btn__oGR_B").click()

        # 서로이웃을 신청합니다 클릭
        driver.find_element(By.CSS_SELECTOR, "#bothBuddyRadio").click()
        time.sleep(1)

        # 메세지란에 기본 메세지 삭제하고 글귀 추가하기
        input_message = "재테크에 관심있는 블로거 입니다. 반갑습니다 ㅎㅎ :)"
        textarea = driver.find_element(By.CSS_SELECTOR, ".textarea_t1")
        textarea.send_keys(Keys.CONTROL, 'a')                                   # Ctrl + a 전체선택
        time.sleep(1)
        textarea.send_keys(Keys.DELETE)                                         # 메세지란 지우기.
        time.sleep(1)
        textarea.send_keys(input_message)                   
        time.sleep(1)

        # 확인 버튼 클릭.
        driver.find_element(By.CSS_SELECTOR, ".btn_ok").click()

    except :
        pass

    # 새 창 닫기
    driver.close()

    # 기존 창으로 드라이버 전환
    driver.switch_to.window(all_windows[0])
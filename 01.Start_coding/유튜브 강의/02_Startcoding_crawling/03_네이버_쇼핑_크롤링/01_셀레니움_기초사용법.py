from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time         # time 딜레이 함수때 필요한 라이브러리

# 브라우저 생성
browser = webdriver.Chrome('C:/chromedriver.exe')

# 웹사이트 열기
browser.get('https://www.naver.com/')            # 네이버를 셀레니움 웹드라이브로 열라는 코드.

# 로딩 딜레이 주기
browser.implicitly_wait(3)     # 로딩이 끝날떄까지 3초까지 기다리기. 로딩이 끝나면 안기다리고 다음작업수행

# 쇼핑 메뉴 클릭
browser.find_element_by_css_selector('a.nav.shop').click()  # 엘리먼트 찾기 및 클릭

# 딜레이
time.sleep(2)

# 검색창 클릭
# search = browser.find_element_by_css_selector('input.co_srh_input._input')  # 엘리먼트 찾기1
search = browser.find_element_by_css_selector('.co_srh_input._input')  # 엘리먼트 찾기2
search.click()      # CSS 클릭


# 검색어 입력
search.send_keys('아이폰 13')               # 아이폰13을 입력
search.send_keys(Keys.ENTER)                # 키보드의 ENTER를 입력

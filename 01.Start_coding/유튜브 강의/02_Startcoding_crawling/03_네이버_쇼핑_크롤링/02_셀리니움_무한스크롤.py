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
search.send_keys('아이폰 13')
search.send_keys(Keys.ENTER)

# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY")         # 브라우저의 자바스크립트를 실행해주는 명령어, 브라우저의 Console에 window.scrollY를 입력하면 현재 스크롤의 위치에 대한 픽셀정보가 나온다.

# 무한 스크롤
while True : 
    # 맨 아래로 스크롤을 내린다.
    browser.find_element_by_css_selector("body").send_keys(Keys.END)    # body 엘리먼트를 찾고, 키보드의 END키를 입력 -> 스크롤이 내려감

    # 스크롤 사이 페이지 로딩 시간 -> 한번에 내려버리면 부하가 걸릴 수 있기 때문
    time.sleep(1)

    # 스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")

    if after_h == before_h :
        break

    before_h = after_h

# 상품 정보 div         클래스에 해당하는 모든 정보를 items에 리스트형태로 저장한다.
items = browser.find_elements_by_css_selector(".basicList_info_area__17Xyo")

for item in items:
    name = item.find_element_by_css_selector(".basicList_title__3P9Q7").text       # 해당클래스의 텍스트정보 가져오기
    
    try:        # 먼저 시도하는 것.
        price = item.find_element_by_css_selector(".price_num__2WUXn").text          
    except:     # 먼저 시도하는 것에서 오류가 날 시 except를 실행한다.
        price = "판매중단"
    
    link = item.find_element_by_css_selector(".basicList_title__3P9Q7 > a").get_attribute('href')   #해당클래스안의 a태그를 찾아 get_attribute를 이용하여 a태그 안의 속성값 불러오기.

    print(name, price, link)





from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기, 부착된 장치가 작동하지 않습니다 등.....
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())      #크롬드라이버매니저를 이용해서 크롬드라이버를 최신버전으로 자동으로 설치해줌
driver = webdriver.Chrome(service=service, options=chrome_options)

# 주소 이동
driver.get("https://www.naver.com")




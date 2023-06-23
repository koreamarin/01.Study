import requests
from bs4 import BeautifulSoup
import pyautogui

codes = ['005930', '000660', '035720']

for code in codes :
    url = f"https://finance.naver.com/item/sise.naver?code={code}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    present_price_tag= soup.select_one("#_nowVal")

    present_price = present_price_tag.text
    #자료형.replace(문자열1, 문자열2)은 자료형에 들어있는 문자열1을 문자열2로 대체하여준다.
    present_price = present_price.replace(',', '')
    print(present_price)
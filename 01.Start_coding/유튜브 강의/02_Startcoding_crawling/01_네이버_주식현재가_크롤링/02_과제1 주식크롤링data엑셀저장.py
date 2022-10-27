# 주식 현재가 크롤링했던 현재가 데이터를 아래 양식의 엑셀을 불러와서 B2, B3, B4에 저장해보자

#        A           B           C               D        E              F          G
#   1    종목        현재가      평균매입가      잔고수량   평가금액        평가손익    수익률
#   2    삼성전자                85,000         20                                      
#   3    SK하이닉스              120,000        15
#   4    카카오                  145,000        10

import requests
from bs4 import BeautifulSoup
import openpyxl

fpath = r'C:\Users\USER\OneDrive\바탕 화면\python\startcoding\유튜브 강의\02_Startcoding_crawling\01_네이버_주식현재가_크롤링\data.xlsx'

codes = ['005930', '000660', '035720']

wb = openpyxl.load_workbook(fpath)
# ws = wb['Sheet1']
ws = wb.active  # 현재 활성화된 시트 선택

row=2

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

    ws[f'B{row}'] = int(present_price)
    row=row+1

wb.save(fpath)
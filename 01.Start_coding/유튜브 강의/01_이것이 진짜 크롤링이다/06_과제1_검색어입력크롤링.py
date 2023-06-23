# 프로그램을 실행하면 검색어를 입력 받게 해서 해당 검색어로 크롤링 되는 프로그램
import requests
from bs4 import BeautifulSoup

def crawling(crawling_url) :
    response = requests.get(crawling_url)

    html = response.text

    soup = BeautifulSoup(html,'html.parser')

    links = soup.select(".news_tit")

    for link in links :
        title = link.text
        url = link.attrs['href']
        print(title, url)



search_word = input("뉴스 페이지를 크롤링할 검색어를 입력해 주세요 >>> ")

crawling_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + search_word

crawling(crawling_url)


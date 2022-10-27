# 내가 원하는 페이지까지 크롤링 하기 ex)1~10페이지
import requests
from bs4 import BeautifulSoup
import pyautogui


# 검색어와 페이지를 입력하면 크롤링하는 함수
def crawling(crawling_url) :
    response = requests.get(crawling_url)

    html = response.text

    soup = BeautifulSoup(html,'html.parser')

    links = soup.select(".news_tit")

    for link in links :
        title = link.text
        url = link.attrs['href']
        print(title, url)


# 검색어입력
# search_word = input("뉴스 페이지를 크롤링할 검색어를 입력해 주세요 >>> ")
search_word = pyautogui.prompt("뉴스 페이지를 크롤링할 검색어를 입력해 주세요 >>> ")

# 페이지입력
# page_min = int(input("크롤링을 시작할 첫번째 페이지를 입력하세요 >>> "))
# page_max = int(input("크롤링을 마칠 마지막 페이지를 입력하세요   >>> "))
page_min = int(pyautogui.prompt("크롤링을 시작할 첫번째 페이지를 입력하세요 >>> "))
page_max = int(pyautogui.prompt("크롤링을 마칠 마지막 페이지를 입력하세요   >>> "))
page = []


# 페이지 계산식
for i in range(page_min,page_max+1) : 
    page.append((i * 10) - 9)


# URL 완성 및 함수부르기
for i in range(len(page)) : 
    #crawling_url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search_word + "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=54&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=" + str(page[i])
    crawling_url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search_word}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=54&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={page[i]}"
    print((page[i]+9)/10, "페이지 크롤링 결과 입니다.")
    crawling(crawling_url)
    print("\n")
import requests
from bs4 import BeautifulSoup

# 네이버에서 프로그램사용자로 인식하여 'Connection aborted.'라는 오류를 띄우고 사용자를 막을 수 있다.
# 딕셔너리를 이용하여 헤더를 만들어서 모질라 웹브라우저로 접속한 것처럼 만들어줄 수 있다.
header = {'User-agent' : 'Mozila/2.0'}

# 네이버에 URL에 대한 요청(requests)을 보낼 때 두번째 인자로 header를 추가하여 모질라로 접속한것처럼 만든 것.
response = requests.get("https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100", headers=header)

# 네이버에서 웹브라우저에 대한 소스가 response에 저장되어 있는데 그 중 text만 뽑아서 html 코드만 뽑음.
html = response.text

# html 구조 분석 프로그램(parser)으로 수프 만듦
# Beautifulsoup(html 코드, html 구조분석 프로그램)
soup = BeautifulSoup(html, 'html.parser')

# class 값이 lik_hdline_article인 놈 한개를 찾아냄
# select_one은 한개의 태그를 선택하고 싶을 때 사용.
# class의 속성으로 select할 때는 .으로 대체하여 쓰도록 한다.
title = soup.select_one('.lik_hdline_article')

# 요청을 보낸 URL의 class : lik_hdline_article를 찾아 text부분만 출력. strip()은 양쪽 공백을 제거한다는 뜻.
print(title.text.strip())



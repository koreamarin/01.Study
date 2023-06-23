 # Beautifulsoup(html 코드, html 번역선생님) --> 이것을 사용하면 아름다운 수프가 완성된다고 함...뭔뜻..?

import requests
from bs4 import BeautifulSoup

# 네이버 서버에 대화를 시도
response = requests.get("https://www.naver.com")

# 네이버에서 html을 줌
html = response.text

# html 번역선생님으로 수프 만듦
# # Beautifulsoup(html 코드, html 번역선생님)
soup = BeautifulSoup(html, 'html.parser')

# id 값이 NM_set_home_btn인 놈 한개를 찾아냄
# select는 여러개의 태그를 선택하고 싶을 때 사용.
# select_one은 한개의 태그를 선택하고 싶을 때 사용.
# id의 속성으로 select할 때는 #으로 대체하여 쓰도록 한다.
word = soup.select_one('#NM_set_home_btn')

# id = NM_set_home_btn에 해당하는 a 태그 자체가 전부 출력이 된다. 
print(word)

print("\n")

# id = NM_set_home_btn에 있는 텍스트 부분만 출력한다.
print(word.text)

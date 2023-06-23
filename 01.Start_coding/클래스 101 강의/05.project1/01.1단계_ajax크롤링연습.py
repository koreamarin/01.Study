import requests
import json

response = requests.get("https://ac.search.naver.com/nx/ac?q=%EC%A3%BC%EC%8B%9D%20%E3%84%B1&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100&_callback=_jsonp_5")
origin_data = response.text
str_data = origin_data.split("_jsonp_5(")[1][:-1]       # 데이터를 split 함수로 나눔. [:-1] 슬라이싱을 사용하여 맨 마지막 문자는 제외하고 str_data에 담음
print(type(str_data))                                   # 타입출력. 타입이 str로 나옴
dic_data = json.loads(str_data)                         # json모듈을 이용하여 문자열을 넣어주면 딕셔너리 형태로 바꿀 수 있음.
print(type(dic_data))



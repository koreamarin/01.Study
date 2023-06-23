import requests
import json
import pyautogui

sub_list = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
main_keyword = pyautogui.prompt("키워드를 입력해주세요")

f = open()

for sub in sub_list :
    keyword = main_keyword + ' ' + sub
    print(keyword)
    response = requests.get(f"https://ac.search.naver.com/nx/ac?q={keyword}&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100&_callback=_jsonp_5")
    origin_data = response.text
    str_data = origin_data.split("_jsonp_5(")[1][:-1]       # 데이터를 split 함수로 나눔. [:-1] 슬라이싱을 사용하여 맨 마지막 문자는 제외하고 str_data에 담음
    dic_data = json.loads(str_data)                         # json모듈을 이용하여 문자열을 넣어주면 딕셔너리 형태로 바꿀 수 있음.
    print(dic_data['items'][0])                             # dic_data의 items 키와 value만 추출. 3차원 리스트이므로 첫번째 인덱스만 추출하여 2차원 리스트로 추출함.
    for data in dic_data['items'][0] :                      # dic_data['items'][0] 리스트의 인덱스를 하나씩 추출하여 print문으로 출력
        print(data[0])
    print()


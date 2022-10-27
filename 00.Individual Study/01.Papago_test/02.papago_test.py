import os
import sys
import requests
from pprint import pprint

client_id = "5x4Icl9wlj1q88yIz16f"
client_secret = "zDuUm4fRWF"

def get_translate(text, lan):
    data = {'text' : text,
            'source' : 'ko',
            'target': lan}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code

    if(rescode==200):
        t_data = response.json()
        pprint(t_data['message']['result']['translatedText'])
    else:
        print("Error Code :" , rescode)


text = input("한국말 : ")
lan = input("번역할 언어 (영어 : en, 일어 : ja) :")
print(get_translate(text, lan))
import os
import sys
import json
import urllib.request

client_id = "5x4Icl9wlj1q88yIz16f"
client_secret = "zDuUm4fRWF"

encText = urllib.parse.quote("hi")
data = "source=en&target=ko&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
    print("에러코드:" + str(rescode))
    print(json.loads(response_body)['message']['result']['translatedText'])
else:
    print("에러코드:" + str(rescode))
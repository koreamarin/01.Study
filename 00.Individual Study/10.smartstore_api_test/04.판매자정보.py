import bcrypt, pybase64, time, requests, datetime
from urllib import parse

def 전자서명발급(client_id, clientSecret, timestamp) :
    password = client_id + "_" + timestamp                                              # 밑줄로 연결하여 password 생성
    hashed = bcrypt.hashpw(password.encode('utf-8'), clientSecret.encode('utf-8'))      # bcrypt 해싱
    return pybase64.standard_b64encode(hashed).decode('utf-8')

def 인증토큰발급(client_id, client_secret_sign, timestamp) :
    request_url = f"https://api.commerce.naver.com/external/v1/oauth2/token?client_id={client_id}&timestamp={timestamp}&client_secret_sign={client_secret_sign}&grant_type=client_credentials&type=SELF"
    response = requests.post(request_url)
    return response.json()['access_token']

def 전자서명_인증토큰_통합발급(client_id, clientSecret) : 
    timestamp = str(round(time.time() * 999.9999984))                              # 5분간 유효
    client_secret_sign = 전자서명발급(client_id, clientSecret, timestamp)           # 전자서명 생성 함수 실행
    access_token = 인증토큰발급(client_id, client_secret_sign, timestamp)           # 인증토큰 발급 함수 실행
    headers = {f"Authorization": f"Bearer {access_token}"}                         # Authorization: Bearer {인증 토큰}
    return headers

def url_maker(request_url, query_parameters=None) :
    api_url = "https://api.commerce.naver.com/external"
    if query_parameters != None :
        query_parameter_url = '?'
        for key,val in query_parameters.items() :
            if val == None :
                continue
            query_parameter_url = f"{query_parameter_url}{key}={val}&"
        completed_url = api_url + request_url + query_parameter_url
    else : 
        completed_url = api_url + request_url
    return completed_url

#########################################판매자정보#####################################################
# 판매자
def 계정으로채널정보조회() :    # 미완성
    request_url = f"/v1/seller/channels"
    completed_url = url_maker(request_url)
    response = requests.get(completed_url, headers=headers)
    return response


# 판매자 오늘출발 설정
def 오늘출발설정정보조회() :    # 미완성
    return 0

def 오늘출발정보설정() :    # 미완성
    return 0


# 판매자 주소록
def 주소록페이징조회() :    
    request_url = f"/v1/seller/addressbooks-for-page"
    completed_url = url_maker(request_url)
    response = requests.get(completed_url, headers=headers)
    return response

def 주소록단건조회() :    # 미완성
    return 0


# 판매자 풀필먼트
def 물류사연동정보조회() :    # 미완성
    return 0

############################################################### main ###############################################

client_id = "1i1BHjBtMPeuDDxnq29cuZ"
clientSecret = "$2a$04$kd3zjeWr6u3i7RY3rf97ye"
headers = 전자서명_인증토큰_통합발급(client_id, clientSecret)

response = 계정으로채널정보조회()
print(response)
print(response.json())

response = 주소록페이징조회()
print(response)
print(response.json())
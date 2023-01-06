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
    timestamp = str(round(time.time() * 999.9999984))                            # 5분간 유효
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

#########################################문의#####################################################
# 고객 문의 답변 등록/수정
def 고객문의답변등록(inquiryNo) :    # 미완성       ################# 개발 필요 ###########
    return 0

def 고객문의답변수정(inquiryNo) :    # 미완성       ################# 개발 필요 ###########
    return 0


# 고객 문의 답변 조회
def 고객문의답변조회(startSearchDate, endSearchDate, page=1, size=10, answered=None) :
    # startSearchDate : 문의검색시작날짜 (str yyyy-MM-dd)
    # endSearchDate : 문의검색종료날짜 (str yyyy-MM-dd)
    # page : 조회할 페이지 번호(integer [1~1000000])
    # size : 페이지 크기(페이지당 10~200건의 문의를 조회할 수 있다)(integer [ 10 .. 200 ])
    # answered : 답변이 완료된 문의 여부(str true/false). 생략 시, 답변 완료 여부에 상관없이 모든 문의를 조회합니다
    request_url = "/v1/pay-user/inquiries"
    query_parameters = {
        'startSearchDate' : startSearchDate,
        'endSearchDate' : endSearchDate,
        'page' : page,
        'size' : size,
        'answered' : answered
    }
    completed_url = url_maker(request_url, query_parameters)
    response = requests.get(completed_url, headers=headers)
    return response


# 상품문의
def 상품문의목록조회(fromDate, toDate, page=1, size=100, answered=None) :
    # startSearchDate : 문의검색시작날짜 (str yyyy-MM-dd)
    # endSearchDate : 문의검색종료날짜 (str yyyy-MM-dd)
    # page : 조회할 페이지 번호(integer [default:1])
    # size : 페이지 크기(integer [MAX:100, default:100])
    # answered : 답변이 완료된 문의 여부(str true/false). 생략 시, 답변 완료 여부에 상관없이 모든 문의를 조회합니다
    request_url = "/v1/contents/qnas"
    fromDate =  f'{fromDate}T00:00:00.0+09:00'      # ISO-8601 형식이어야함.
    toDate =    f'{toDate}T00:00:00.0+09:00'        # ISO-8601 형식이어야함.
    fromDate =  parse.quote(fromDate)               # url encoding
    toDate =    parse.quote(toDate)                 # url encoding
    query_parameters = {
        'fromDate' : fromDate,
        'toDate' : toDate,
        'page' : page,
        'size' : size,
        'answered' : answered
    }
    completed_url = url_maker(request_url, query_parameters)
    response = requests.get(completed_url, headers=headers)
    return response

def 상품문의답변템플릿목록조회() : 
    request_url = "/v1/contents/qnas/templates"
    completed_url = url_maker(request_url)
    response = requests.get(completed_url, headers=headers)
    return response

def 상품문의답변등록수정(questionId, commentContent) :
    # questionId : integer <int64> 상품 문의 ID
    # commentContent : 	string (상품 문의 답변 내용)
    request_url = f"/v1/contents/qnas/{questionId}"
    completed_url = url_maker(request_url)
    headers['content-type'] = "application/json"
    json = {
        'commentContent' : commentContent
        }
    response = requests.put(completed_url, headers=headers, json=json)
    return response

###############################################################  main  ###############################################

client_id = "1i1BHjBtMPeuDDxnq29cuZ"
clientSecret = "$2a$04$kd3zjeWr6u3i7RY3rf97ye"
headers = 전자서명_인증토큰_통합발급(client_id, clientSecret)

# startSearchDate = '2022-11-01'
# endSearchDate = '2022-12-08'
# response = 고객문의답변조회(startSearchDate, endSearchDate)
# print(response)
# print(response.json())

# print()

# fromDate = '2022-10-24'
# toDate = '2022-12-09'
# response = 상품문의목록조회(fromDate, toDate)
# print(response)
# print(response.json())

# print()

# response = 상품문의답변템플릿목록조회()
# print(response)
# print(response.json())

# print()

# questionId = 504786209
# commentContent = '안녕하세요. 고객님. 현재 품절된 상품입니다. 불편을 드려 죄송합니다.'
# response = 상품문의답변등록수정(questionId, commentContent)
# print(response)
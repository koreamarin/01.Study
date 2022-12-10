import bcrypt, pybase64, time, requests

def 전자서명발급(client_id, clientSecret, timestamp) :
    password = client_id + "_" + timestamp                                              # 밑줄로 연결하여 password 생성
    hashed = bcrypt.hashpw(password.encode('utf-8'), clientSecret.encode('utf-8'))      # bcrypt 해싱
    return pybase64.standard_b64encode(hashed).decode('utf-8')

def 인증토큰발급(client_id, client_secret_sign, timestamp) :
    request_url = f"https://api.commerce.naver.com/external/v1/oauth2/token?client_id={client_id}&timestamp={timestamp}&client_secret_sign={client_secret_sign}&grant_type=client_credentials&type=SELF"
    response = requests.post(request_url)
    return response.json()['access_token']

def 전자서명_인증토큰_통합발급(client_id, clientSecret) : 
    timestamp = str(round(time.time() * 999.999998665))                            # 5분간 유효
    client_secret_sign = 전자서명발급(client_id, clientSecret, timestamp)           # 전자서명 생성 함수 실행
    access_token = 인증토큰발급(client_id, client_secret_sign, timestamp)           # 인증토큰 발급 함수 실행
    headers = {f"Authorization": f"Bearer {access_token}"}                         # Authorization: Bearer {인증 토큰}
    return headers



#########################################문의#####################################################
# 고객 문의 답변 등록/수정
def 고객문의답변등록(inquiryNo) :    # 미완성
    request_url = f'https://api.commerce.naver.com/external/v1/pay-merchant/inquiries/{inquiryNo}/answer'
    return 0

def 고객문의답변수정() :    # 미완성
    return 0


# 고객 문의 답변 조회
def 고객문의답변조회(startSearchDate, endSearchDate) :  # 문의검색시작날짜 (yyyy-MM-dd), 문의검색종료날짜 (yyyy-MM-dd)
    request_url = f"https://api.commerce.naver.com/external/v1/pay-user/inquiries?startSearchDate={startSearchDate}&endSearchDate={endSearchDate}"
    response = requests.get(request_url, headers=headers)
    return response


# 상품문의
def 상품문의목록조회() :    # 미완성
    return 0

def 상품문의답변템플릿목록조회() :    # 미완성
    return 0

def 상품문의답변등록수정() :    # 미완성
    return 0


#########################################상품#####################################################
# 모델
def 모델조회() :    # 미완성
    return 0


def 모델단건조회() :    # 미완성
    return 0


# 브랜드
def 브랜드조회() :    # 미완성
    return 0


# 상품
def 상품등록() :    # 미완성 V2 사용
    return 0

def 채널상품조회() :    # 미완성 V2 사용
    return 0

def 채널상품수정() :    # 미완성 V2 사용
    return 0

def 채널상품삭제() :    # 미완성 V2 사용
    return 0

def 상품벌크업데이트() :    # 미완성
    return 0

def 원상품조회() :    # 미완성 V2 사용
    return 0

def 원상품수정() :    # 미완성 V2 사용
    return 0

def 원상품삭제() :    # 미완성 V2 사용
    return 0

def 판매상태변경() :    # 미완성
    return 0


#  상품 검수
def 수정요청삼품에대해복원요청() :      # 미완성
    return 0

def 수정요청상품목록을조회() :    # 미완성
    return 0


# 상품 공지사항
def 공지사항목록조회() :    # 미완성
    return 0

def 공지사항등록() :    # 미완성
    return 0

def 공지사항단건조회() :    # 미완성
    return 0

def 공지사항수정() :    # 미완성
    return 0

def 공지사항삭제() :    # 미완성
    return 0


# 상품 공지사항 적용
def 채널상품공지사항적용 () :   # 미완성
    return 0


# 상품 목록
def 상품목록조회() :    # 미완성
    return 0


# 상품배송정보
def 묶음배송그룹다건조회() :    # 미완성
    return 0

def 묶음배송그룹등록() :    # 미완성
    return 0

def 묶음배송그룹단건조회() :    # 미완성
    return 0

def 묶음배송그룹수정() :    # 미완성
    return 0

def 희망일배송그룹다건조회() :    # 미완성
    return 0

def 희망일배송그룹등록() :    # 미완성
    return 0

def 희망일배송그룹단건조회() :    # 미완성
    return 0

def 희망일배송그룹수정() :    # 미완성
    return 0

def 반품택배사다건조회() :    # 미완성
    return 0


# 상품 속성
def 전체속성값단위조회() :    # 미완성
    return 0

def 카테고리별속성값조회() :    # 미완성
    return 0

def 카테고리별속성조회() :    # 미완성
    return 0


# 상품 원산지정보
def 원산지코드정보전체조회() :    # 미완성
    return 0

def 원산지코드정보다건조회() :    # 미완성
    return 0

def 하위원산지코드정보다건조회() :    # 미완성
    return 0


# 상품 이미지
def 상품이미지다건등록() :    # 미완성
    return 0


# 옵션
def 카테고리별표준옵션조회() :    # 미완성
    return 0


# 제조사
def 제조사조회() :    # 미완성
    return 0


# 카테고리
def 전체카테고리조회() :    # 미완성
    return 0

def 카테고리조회() :    # 미완성
    return 0

def 하위카테고리조회() :    # 미완성
    return 0

#########################################주문#####################################################
# 교환
def 교환재배송처리() :    # 미완성
    return 0


# 발주/발송 처리
def 발주확인처리() :    # 미완성
    return 0

def 발송처리() :    # 미완성
    return 0

def 발송지연처리() :    # 미완성
    return 0

def 배송희망일변경처리() :    # 미완성
    return 0


# 주문 조회
def 상품주문목록조회() :    # 미완성
    return 0

def 변경상품주문내역조회() :    # 미완성
    return 0

def 상품주문상세내역조회() :    # 미완성
    return 0


# 취소
def 취소요청승인() :    # 미완성
    return 0

#########################################판매자정보#####################################################
# 판매자
def 계정으로채널정보조회() :    # 미완성
    return 0


# 판매자 오늘출발 설정
def 오늘출발설정정보조회() :    # 미완성
    return 0

def 오늘출발정보설정() :    # 미완성
    return 0


# 판매자 주소록
def 주소록페이징조회() :    # 미완성
    return 0

def 주소록단건조회() :    # 미완성
    return 0


# 판매자 풀필먼트
def 물류사연동정보조회() :    # 미완성
    return 0




client_id = "1i1BHjBtMPeuDDxnq29cuZ"
clientSecret = "$2a$04$kd3zjeWr6u3i7RY3rf97ye"
headers = 전자서명_인증토큰_통합발급(client_id, clientSecret)




startSearchDate = '2022-11-01'
endSearchDate = '2022-12-08'
response = 고객문의답변조회(startSearchDate, endSearchDate)

print(response)
print(response.json())
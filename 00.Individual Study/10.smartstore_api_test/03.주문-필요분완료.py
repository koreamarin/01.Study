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

#########################################주문#####################################################
# 교환
def 교환재배송처리() :    # 미완성
    return 0


# 발주/발송 처리
def 발주확인처리(productOrderIds) :
    # productOrderIds : 상품 주문 번호 배열, Array of strings (arrayOfString.pay-order-seller)
    request_url = "/v1/pay-order/seller/product-orders/confirm"
    completed_url = url_maker(request_url)
    headers['content-type'] = "application/json"
    json = {
        'productOrderIds' : productOrderIds
    }
    response = requests.post(completed_url, headers=headers, json=json)
    return response

def 발송처리(productOrderId, dispatchDate ,deliveryMethod, deliveryCompanyCode=None, trackingNumber=None) :
    # productOrderId : 상품 주문 번호. string 형식
    # dispatchDate : 배송일 string 형식 <date-time>     2022-10-10T11:55:59.000Z
    # deliveryMethod : 배송 방법 코드. 250바이트 내외. string 형식
                    # 코드	            설명
                    # DELIVERY	        택배, 등기, 소포	
                    # GDFW_ISSUE_SVC	굿스플로 송장 출력	
                    # VISIT_RECEIPT	    방문 수령	
                    # DIRECT_DELIVERY	직접 전달	
                    # QUICK_SVC	        퀵서비스	
                    # NOTHING	        배송 없음	
                    # RETURN_DESIGNATED	지정 반품 택배	
                    # RETURN_DELIVERY	일반 반품 택배	
                    # RETURN_INDIVIDUAL	직접 반송	
                    # RETURN_MERCHANT	판매자 직접 수거	
                    # UNKNOWN	        알 수 없음(예외 처리에 사용)	
    # deliveryCompanyCode : 택배사 코드. string 형식 (택배사 코드 api 참고)
    # trackingNumber : 송장 번호. string 형식
    request_url = "/v1/pay-order/seller/product-orders/dispatch"
    dispatchDate =  f'{dispatchDate}T11:55:59.000Z'      # ISO-8601 형식이어야함.
    json = {
                "dispatchProductOrders" :   [
                    {
                        'productOrderId' : productOrderId,
                        'deliveryMethod' : deliveryMethod,
                        'deliveryCompanyCode' : deliveryCompanyCode,
                        'trackingNumber' : trackingNumber,
                        'dispatchDate' : dispatchDate
                    }
                ]
            }
    completed_url = url_maker(request_url)
    headers['content-type'] = "application/json"
    response = requests.post(completed_url, headers=headers, json=json)
    return response

def 발송지연처리() :    # 미완성
    return 0

def 배송희망일변경처리() :    # 미완성
    return 0


# 주문 조회
def 상품주문목록조회(orderId) :    # 주문번호(orderId)를 넣으면 상품주문번호(productOrderIds)가 나옴.
    # orderId : 주문번호 string 형식
    request_url = f"/v1/pay-order/seller/orders/{orderId}/product-order-ids"
    completed_url = url_maker(request_url)
    response = requests.get(completed_url, headers=headers)
    return response

def 변경상품주문내역조회(lastChangedFrom, lastChangedTo=None, lastChangedType=None, moreSequence=None, limitCount=None) :
    # lastChangedFrom : 조회시작일시 - 마지막변경일시를 기준으로 조회종료일시를 설정하는 란. datatime 형식 사용.
    # lastChangedTo :   조회종료일시 - 마지막변경일시를 기준으로 조회종료일시를 설정하는 란. datatime 형식 사용. 입력하지 않으면 lastChangedFrom부터 24시간 후로 자동 적용.
    # lastChangedType : 최종변경구분 - 마지막변경을 어떤 타입을 볼건지 설정하는 필터이다. str 형식 사용.
                        # PAY_WAITING	            결제 대기	
                        # PAYED	                    결제 완료	
                        # EXCHANGE_OPTION	        옵션 변경
                        # DELIVERY_ADDRESS_CHANGED	배송지 변경	
                        # GIFT_RECEIVED	            선물 수락
                        # CLAIM_REJECTED	        클레임 철회	
                        # DISPATCHED	            발송 처리	
                        # CLAIM_REQUESTED	        클레임 요청	
                        # COLLECT_DONE	            수거 완료	
                        # CLAIM_HOLDBACK_RELEASED	클레임 보류 해제	
                        # CLAIM_COMPLETED	        클레임 완료	
                        # PURCHASE_DECIDED	        구매 확정
    # moreSequence :    뭔지 모르겠음.
    # limitCount :      조회 응답 개수 제한. 생략하거나 300을 초과하는 값을 입력하면 최대 300개의 내역을 제공합니다. integer 형식 사용.
    # 추가 설명 : 이 함수는 상품주문내역의 변화가 있는 상품들을 변화된 시간 기준으로 오름차순으로 정렬하여 응답해준다.
                # 깃허브 커뮤니티의 설명을 보면 주기적으로 호출을 진행하라고 하는데 이 이유는 만약 변동내역이 300개 이상인 경우 이 함수가 300번째를 초과하는 변경내역은
                # 응답하지 않아 상품변경내역이 누락되어버리므로 주기적으로 호출을 진행하라고 하는 것이다.
    request_url = "/v1/pay-order/seller/product-orders/last-changed-statuses"
    lastChangedFrom =  f'{lastChangedFrom}T00:00:00.0+09:00'      # ISO-8601 형식이어야함.
    lastChangedFrom =  parse.quote(lastChangedFrom)               # url encoding
    if lastChangedTo != None :
        lastChangedTo =    f'{lastChangedTo}T00:00:00.0+09:00'        # ISO-8601 형식이어야함.
        lastChangedTo =    parse.quote(lastChangedTo)                 # url encoding
    query_parameters = {
        'lastChangedFrom' : lastChangedFrom,
        'lastChangedTo' : lastChangedTo,
        'lastChangedType' : lastChangedType,
        'moreSequence' : moreSequence,
        'limitCount' : limitCount
    }
    completed_url = url_maker(request_url, query_parameters)
    response = requests.get(completed_url, headers=headers)
    return response

def 상품주문상세내역조회(productOrderIds) :
    # productOrderIds : array of strings 상품주문번호
    request_url = "/v1/pay-order/seller/product-orders/query"
    completed_url = url_maker(request_url)
    headers['content-type'] = "application/json"
    json = {
        'productOrderIds' : productOrderIds
    }
    response = requests.post(completed_url, headers=headers, json=json)
    return response


# 취소
def 취소요청승인(productOrderId) : 
    # productOrderId : 상품주문번호. 취소요청건이 들어온 상품주문번호를 입력하면 취소가 승인된다. string 형식
    request_url = f"/v1/pay-order/seller/product-orders/{productOrderId}/claim/cancel/approve"
    completed_url = url_maker(request_url)
    response = requests.post(completed_url, headers=headers)
    return response




############################################################### main ###############################################

client_id = "1i1BHjBtMPeuDDxnq29cuZ"
clientSecret = "$2a$04$kd3zjeWr6u3i7RY3rf97ye"
headers = 전자서명_인증토큰_통합발급(client_id, clientSecret)

# orderId = 2022120955515361
# response = 상품주문목록조회(orderId)
# print(response)
# print(response.json())

print()

productOrderIds = [2022121587675721]
response = 상품주문상세내역조회(productOrderIds)
print(response)
print(response.json())

print()

lastChangedFrom = '2022-12-15'
lastChangedTo = None
lastChangedType = None
moreSequence = None
limitCount = 300
response = 변경상품주문내역조회(lastChangedFrom)
print(response)
print(response.json())

# print()

# productOrderIds = [
#         2022121284429371
#     ]
# response = 발주확인처리(productOrderIds)
# print(response)
# print(response.json())

print()

# productOrderId = 2022121284429371
# dispatchDate = '2022-12-13'
# deliveryMethod = 'DIRECT_DELIVERY'
# deliveryCompanyCode = None
# trackingNumber = None
# response = 발송처리(productOrderId, dispatchDate, deliveryMethod)
# print(response)
# print(response.json())

    # 취소완료
    # 'productOrderId': '2022121142694101'
    # 'orderId': '2022121190572721'
    # 'productOrderStatus': 'CANCELED'
    # 'claimType': 'CANCEL'
    # 'paymentDate': '2022-12-11T23:00:31.0+09:00'
    # 'claimStatus': 'CANCEL_DONE'
    # 'lastChangedDate': '2022-12-13T00:22:14.0+09:00'
    # 'lastChangedType': 'CLAIM_COMPLETED'
    # 'receiverAddressChanged': False

    # 취소요청
    # 'productOrderId': '2022121282456811'
    # 'orderId': '2022121224447761'
    # 'productOrderStatus': 'PAYED'
    # 'claimType': 'CANCEL'
    # 'paymentDate': '2022-12-12T21:18:52.0+09:00'
    # 'claimStatus': 'CANCELING'
    # 'lastChangedDate': '2022-12-13T00:22:25.0+09:00'
    # 'lastChangedType': 'CLAIM_REQUESTED'
    # 'receiverAddressChanged': False

    # 배송중
    # 'productOrderId': '2022121284429371'
    # 'orderId': '2022121225666851'
    # 'productOrderStatus': 'DELIVERING'
    # 'paymentDate': '2022-12-12T22:06:06.0+09:00'
    # 'lastChangedDate': '2022-12-13T01:11:34.0+09:00'
    # 'lastChangedType': 'DISPATCHED'
    # 'receiverAddressChanged': False

print()

# productOrderId = 2022121284429371
# response = 취소요청승인(productOrderId)
# print(response)
# print(response.json())
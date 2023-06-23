import http.client, time, requests, bcrypt, pybase64
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
    return access_token




client_id = "1i1BHjBtMPeuDDxnq29cuZ"
clientSecret = "$2a$04$kd3zjeWr6u3i7RY3rf97ye"

conn = http.client.HTTPSConnection("api.commerce.naver.com")

headers = {
    'Authorization': f"Bearer {전자서명_인증토큰_통합발급(client_id, clientSecret)}",
    'content-type': "application/json"
    }

productOrderId = 2022121284429371
dispatchDate = '2022-12-13T00:00:00.0+09:00'      # ISO-8601 형식이어야함.
dispatchDate = parse.quote(dispatchDate)               # url encoding
deliveryMethod = 'DIRECT_DELIVERY'
deliveryCompanyCode = None
trackingNumber = None

payload = """[
                {
                    \"productOrderId\":\"2022121284429371\",
                    \"deliveryMethod\":\"DIRECT_DELIVERY\",
                    \"deliveryCompanyCode\":\"\",
                    \"trackingNumber\":\"\",
                    \"dispatchDate\":\"2022-04-05T03:17:35.000Z\"
                }
            ]"""

conn.request("POST", "/external/v1/pay-order/seller/product-orders/dispatch", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
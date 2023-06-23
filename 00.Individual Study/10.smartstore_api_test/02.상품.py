import bcrypt, pybase64, time, requests, datetime, os
from urllib import parse
from mimetypes import MimeTypes
from urllib.request import urlopen
from posixpath import split

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

#########################################상품#####################################################
# 모델
def 모델조회(headers) :
    request_url = "/v1/product-models"
    completed_url = url_maker(request_url)
    response = requests.get(completed_url, headers=headers)
    return response

# 카테고리
def 전체카테고리조회() : 
    request_url = "/v1/categories"
    query_parameters = {
        'last' : True
    }
    completed_url = url_maker(request_url, query_parameters)
    response = requests.get(completed_url, headers=headers)
    return response

# 상품 원산지정보
def 원산지코드정보전체조회(headers) :  
    request_url = "/v1/product-origin-areas"
    completed_url = url_maker(request_url)
    response = requests.get(completed_url, headers=headers)
    return response

# 상품 이미지
def 상품이미지다건등록(headers, img_path_list) : 
    print("multi_image_upload")

    if len(img_path_list) > 10:
        print("이미지수", len(img_path_list))
        print("이미지는 최대 10개까지만 등록가능합니다.")
        return

    request_url = "/v1/product-images/upload"
    completed_url = url_maker(request_url)

    files = {}
    for i in range(len(img_path_list)):
        img_path = img_path_list[i]
        img_name = os.path.basename(img_path)
        img_type = get_mime_type(img_path)
        img_binary = open(img_path, "rb").read()
        files.update({f"imageFiles[{i}]": (f"{img_name}", img_binary, img_type)})

    response = requests.post(completed_url, headers=headers, files=files)
    return response

def URL상품이미지다건등록(headers, img_URL_list) : 
    print("multi_image_upload")

    if len(img_URL_list) > 10:
        print("이미지수", len(img_URL_list))
        print("이미지는 최대 10개까지만 등록가능합니다.")
        return
        
    request_url = "/v1/product-images/upload"
    completed_url = url_maker(request_url)

    files = {}
    for i in range(len(img_URL_list)):
        img_URL = img_URL_list[i]
        img_name = img_URL.split('?')[0].split('/')[-1]
        img_type = get_mime_type(img_name)
        img_binary= urlopen(img_URL).read()
        files.update({f"imageFiles[{i}]": (f"{img_name}", img_binary, img_type)})

    response = requests.post(completed_url, headers=headers, files=files)
    return response

# 상품
def 상품등록(headers, name, thumbnail_img_url, detailContent, salePrice, stockQuantity, shippingAddressId, returnAddressId,afterServiceTelephoneNumber, afterServiceGuideContent, originAreaCode, content, sellerManagementCode, producer, manufacturerName, brandName, modelName) :    # 미완성 V2 사용        ################# 개발 필요 ###########
    response = URL상품이미지다건등록(headers, thumbnail_img_url)
    response_img_URL_list = response.json()['images']

    representativeImage = response_img_URL_list[0]
    optionalImages = response_img_URL_list[1:len(response_img_URL_list)]

    request_url = "/v2/products"
    completed_url = url_maker(request_url)
    headers['content-type'] = "application/json"
    json = {
        "originProduct":
        {
            "statusType":"SALE",
            "leafCategoryId":"50001735",
            "name":name,
            "images":
            {
                "representativeImage":representativeImage,
                "optionalImages":optionalImages
            },
            "detailContent":detailContent,
            "salePrice":salePrice,
            "stockQuantity":stockQuantity,
            "deliveryInfo":
            {
                "deliveryType":"DIRECT",
                "deliveryAttributeType":"NORMAL",
                "deliveryFee":{},
                "claimDeliveryInfo":
                {
                    "returnDeliveryCompanyPriorityType":"PRIMARY",
                    "returnDeliveryFee":0,
                    "exchangeDeliveryFee":0,
                    "shippingAddressId":shippingAddressId,
                    "returnAddressId":returnAddressId,
                    "freeReturnInsuranceYn":False
                },
                "installationFee":False,
            },
            "detailAttribute":
            {   
                "naverShoppingSearchInfo":
                {
                    "manufacturerName":manufacturerName,
                    "brandName":brandName,
                    "modelName":modelName
                },
                "afterServiceInfo":
                {
                    "afterServiceTelephoneNumber":afterServiceTelephoneNumber,
                    "afterServiceGuideContent":afterServiceGuideContent
                },
                "purchaseQuantityInfo":
                {
                    "maxPurchaseQuantityPerOrder":1
                },
                "originAreaInfo":
                {
                    "originAreaCode":originAreaCode,
                    "content":content
                },
                "sellerCodeInfo":
                {
                    "sellerManagementCode":sellerManagementCode,
                },
                "taxType":"TAX",
                "minorPurchasable":True,
                "productInfoProvidedNotice":
                {
                    "productInfoProvidedNoticeType":"DIGITAL_CONTENTS",
                    "digitalContents":
                    {
                        "returnCostReason":0,
                        "noRefundReason":0,
                        "qualityAssuranceStandard":0,
                        "compensationProcedure":0,
                        "troubleShootingContents":0,
                        "producer":producer,
                        "termsOfUse":"상품상세페이지의 사양 부문 참조",
                        "usePeriod":"없음",
                        "medium":"이메일 발송",
                        "requirement":"상품상세페이지의 사양 부문 참조",
                        "cancelationPolicy":"상세페이지참조",
                        "customerServicePhoneNumber":afterServiceTelephoneNumber
                    }
                },
            },
        },
        
        "smartstoreChannelProduct":
        {
            "naverShoppingRegistration":True,
            "channelProductDisplayStatusType":"ON"
        }
    }
    response = requests.post(completed_url, headers=headers, json=json)
    return response


def 아직사용안함() :
    # 모델
    def 모델단건조회() :    # 미완성
        return 0

    # 브랜드
    def 브랜드조회() :    # 미완성
        return 0

    def 채널상품조회() :    # 미완성 V2 사용    ################# 개발 필요 ###########
        return 0

    def 채널상품수정() :    # 미완성 V2 사용    ################# 개발 필요 ###########
        return 0

    def 채널상품삭제() :    # 미완성 V2 사용    ################# 개발 필요 ###########
        return 0

    def 상품벌크업데이트() :    # 미완성
        return 0

    def 원상품조회() :    # 미완성 V2 사용
        return 0

    def 원상품수정() :    # 미완성 V2 사용
        return 0

    def 원상품삭제() :    # 미완성 V2 사용
        return 0

    def 판매상태변경() :    # 미완성            ################# 개발 필요 ###########
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
    def 원산지코드정보다건조회() :    # 미완성
        return 0

    def 하위원산지코드정보다건조회() :    # 미완성
        return 0



    # 옵션
    def 카테고리별표준옵션조회() :    # 미완성
        return 0


    # 제조사
    def 제조사조회() :    # 미완성
        return 0


    # 카테고리

    def 카테고리조회() :    # 미완성
        return 0

    def 하위카테고리조회() :    # 미완성
        return 0


def get_mime_type(file_path):
    mime = MimeTypes()
    mime_type, encoding = mime.guess_type(file_path)
    return mime_type
###############################################################  main  ###############################################

client_id = "20Yww81pYV278Ml2IZqY9u"
clientSecret = "$2a$04$j9zPfhC4krQF07GYkW7.xe"
headers = 전자서명_인증토큰_통합발급(client_id, clientSecret)

print()

name = "상품명"                 # 상품명
# 썸네일 이미지 리스트
thumbnail_img_url = ["https://cdn.akamai.steamstatic.com/steam/apps/1446780/header.jpg?t=1670323598", "https://cdn.akamai.steamstatic.com/steam/apps/1811260/header.jpg?t=1672758344", "https://cdn.akamai.steamstatic.com/steam/apps/960170/header.jpg?t=1666858912"]
detailContent = "상세페이지"     # 상세페이지
salePrice = 10000               # 판매가격
stockQuantity = 9999            # 재고수량
shippingAddressId = 104954785   # 출고지 주소록 번호
returnAddressId = 104954786     # 반품/교환지 주소록 번호
afterServiceTelephoneNumber = '-' # A/S 전화번호
afterServiceGuideContent = '상세페이지 참조' # A/S 안내
originAreaCode = '04'      # 원산지 코드
content = '상세설명에 표시'
sellerManagementCode = 620      # 판매자 관리코드 ( 게임ID와 연동)
producer = '제작자'
manufacturerName = '제작자'     # 제조사명
brandName = '브랜드명'          # 브랜드명 (제작자)
modelName = '모델명'            # 모델명 (게임이름)

response = 상품등록(headers, name, thumbnail_img_url, detailContent, salePrice, stockQuantity, shippingAddressId, returnAddressId, afterServiceTelephoneNumber, afterServiceGuideContent, originAreaCode, content, sellerManagementCode, producer, manufacturerName, brandName, modelName)           
print(response)
print(response.json())



# img_path_list = [r"C:\Users\USER\OneDrive\바탕 화면\header (1).jpg"]
# response = 상품이미지다건등록(headers, img_path_list)
# print(response)
# print(response.json())


# thumbnail_img_url = ["https://cdn.akamai.steamstatic.com/steam/apps/1446780/header.jpg?t=1670323598", "https://cdn.akamai.steamstatic.com/steam/apps/1811260/header.jpg?t=1672758344", "https://cdn.akamai.steamstatic.com/steam/apps/960170/header.jpg?t=1666858912"]
# response = URL상품이미지다건등록(headers, thumbnail_img_url)
# response_img_URL_list = response.json()['images']
# representativeImage = response_img_URL_list[0]
# optionalImages = response_img_URL_list[1:len(response_img_URL_list)]
# print(representativeImage)
# print(optionalImages)


# response = 전체카테고리조회()
# for i in response.json() :
#     print(f"(명 : {i['name']} / id : {i['id']})", end="/")


# response = 원산지코드정보전체조회(headers)
# print(response)
# print(response.json())

# response = 모델조회(headers)
# print(response)
# print(response.json())




"""
json = {
        "originProduct":
        {
            "statusType":"WAIT",
            "saleType":"NEW",
            "leafCategoryId":"string",
            "name":"string",
            "images":
            {
                "representativeImage":
                {
                    "url":"string"
                },
                "optionalImages":
                    [
                        {
                            "url":"string"
                            }
                    ]
            },
            "detailContent":"string",
            "saleStartDate":"2023-01-03T14:32:30Z",
            "saleEndDate":"2023-01-03T14:32:30Z",
            "salePrice":0,
            "stockQuantity":0,
            "deliveryInfo":
            {
                "deliveryType":"DELIVERY",
                "deliveryAttributeType":"NORMAL",
                "deliveryCompany":"string",
                "deliveryBundleGroupUsable":True,
                "deliveryBundleGroupId":0,
                "quickServiceAreas":["SEOUL"],
                "visitAddressId":0,
                "deliveryFee":
                {
                    "deliveryFeeType":"FREE",
                    "baseFee":0,
                    "freeConditionalAmount":0,
                    "repeatQuantity":0,
                    "secondBaseQuantity":0,
                    "secondExtraFee":0,
                    "thirdBaseQuantity":0,
                    "thirdExtraFee":0,
                    "deliveryFeePayType":"COLLECT",
                    "deliveryFeeByArea":
                    {
                        "deliveryAreaType":"AREA_2",
                        "area2extraFee":0,
                        "area3extraFee":0
                    },
                    "differentialFeeByArea":"string"
                },
                "claimDeliveryInfo":
                {
                    "returnDeliveryCompanyPriorityType":"PRIMARY",
                    "returnDeliveryFee":0,
                    "exchangeDeliveryFee":0,
                    "shippingAddressId":0,
                    "returnAddressId":0,
                    "freeReturnInsuranceYn":True
                },
                "installationFee":True,
                "expectedDeliveryPeriodType":"ETC",
                "expectedDeliveryPeriodDirectInput":"string",
                "todayStockQuantity":0,
                "customProductAfterOrderYn":True,
                "hopeDeliveryGroupId":0
            },
            "productLogistics":
            [
                {
                    "logisticsCompanyId":"string",
                    "logisticsCenterId":"string"
                }
            ],
            "detailAttribute":
            {
                "naverShoppingSearchInfo":
                {
                    "modelId":0,
                    "manufacturerName":"string",
                    "brandName":"string",
                    "modelName":"string"
                },
                "afterServiceInfo":
                {
                    "afterServiceTelephoneNumber":"string",
                    "afterServiceGuideContent":"string"
                },
                "purchaseQuantityInfo":
                {
                    "minPurchaseQuantity":0,
                    "maxPurchaseQuantityPerId":0,
                    "maxPurchaseQuantityPerOrder":0
                },
                "originAreaInfo":
                {
                    "originAreaCode":"string",
                    "importer":"string",
                    "content":"string",
                    "plural":True
                },
                "sellerCodeInfo":
                {
                    "sellerManagementCode":"string",
                    "sellerBarcode":"string",
                    "sellerCustomCode1":"string",
                    "sellerCustomCode2":"string"
                },
                "optionInfo":
                {
                    "simpleOptionSortType":"CREATE",
                    "optionSimple":
                    [
                        {
                            "id":0,
                            "groupName":"string",
                            "name":"string",
                            "usable":True
                        }
                    ],
                    "optionCustom":
                    [
                        {
                            "id":0,
                            "groupName":"string",
                            "name":"string",
                            "usable":True
                        }
                    ],
                    "optionCombinationSortType":"CREATE",
                    "optionCombinationGroupNames":
                    {
                        "optionGroupName1":"string",
                        "optionGroupName2":"string",
                        "optionGroupName3":"string",
                        "optionGroupName4":"string"
                    },
                    "optionCombinations":
                    [
                        {
                            "id":0,
                            "optionName1":"string",
                            "optionName2":"string",
                            "optionName3":"string",
                            "optionName4":"string",
                            "stockQuantity":0,
                            "price":0,
                            "sellerManagerCode":"string",
                            "usable":True
                        }
                    ],
                    "standardOptionGroups":
                    [
                        {
                            "groupName":"string",
                            "standardOptionAttributes":
                            [
                                {"attributeId":0,
                                "attributeValueId":0,
                                "attributeValueName":"string",
                                "imageUrls":["string"]
                                }
                            ]
                        }
                    ],
                    "optionStandards":
                    [
                        {
                            "id":0,
                            "optionName1":"string",
                            "optionName2":"string",
                            "stockQuantity":0,
                            "sellerManagerCode":"string",
                            "usable":True
                        }
                    ],
                    "useStockManagement":True,
                    "optionDeliveryAttributes":["string"]
                },
                "supplementProductInfo":
                {
                    "sortType":"CREATE",
                    "supplementProducts":
                    [
                        {
                            "id":0,
                            "groupName":"string",
                            "name":"string",
                            "price":0,
                            "stockQuantity":0,
                            "sellerManagementCode":"string",
                            "usable":True
                        }
                    ]
                },
                "purchaseReviewInfo":
                {
                    "purchaseReviewExposure":True,
                    "reviewUnExposeReason":"string"
                },
                "isbnInfo":
                {
                    "isbn13":"string",
                    "issn":"string",
                    "independentPublicationYn":True
                },
                "bookInfo":
                {
                    "publishDay":"string",
                    "publisher":
                    {
                        "code":"string",
                        "text":"string"
                    },
                    "authors":
                    [
                        {
                            "code":"string",
                            "text":"string"
                        }
                    ],
                    "illustrators":
                    [
                        {
                            "code":"string",
                            "text":"string"
                        }
                    ],
                    "translators":
                    [
                        {
                            "code":"string",
                            "text":"string"
                        }
                    ]
                },
                "eventPhraseCont":"string",
                "manufactureDate":"2023-01-03",
                "validDate":"2023-01-03",
                "taxType":"TAX",
                "productCertificationInfos":
                [
                    {
                        "certificationInfoId":0,
                        "certificationKindType":"KC_CERTIFICATION",
                        "name":"string",
                        "certificationNumber":"string",
                        "certificationMark":True,
                        "companyName":"string",
                        "certificationDate":"2023-01-03"
                    }
                ],
                "certificationTargetExcludeContent":
                {
                    "childCertifiedProductExclusionYn":True,
                    "kcExemptionType":"OVERSEAS",
                    "kcCertifiedProductExclusionYn":"FALSE",
                    "greenCertifiedProductExclusionYn":True
                },
                "sellerCommentContent":"string",
                "sellerCommentUsable":True,
                "minorPurchasable":True,
                "ecoupon":
                {
                    "periodType":"FIXED",
                    "validStartDate":"2023-01-03",
                    "validEndDate":"2023-01-03",
                    "periodDays":0,
                    "publicInformationContents":"string",
                    "contactInformationContents":"string",
                    "usePlaceType":"PLACE",
                    "usePlaceContents":"string",
                    "restrictCart":True,
                    "siteName":"string"
                },
                "productInfoProvidedNotice":
                {
                    "productInfoProvidedNoticeType":"WEAR",
                    "wear":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "material":"string",
                        "color":"string",
                        "size":"string",
                        "manufacturer":"string",
                        "caution":"string",
                        "packDateType":"CALENDER",
                        "packDate":"string",
                        "packDateText":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "shoes":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "material":"string",
                        "color":"string",
                        "size":"string",
                        "height":"string",
                        "manufacturer":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "bag":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "type":"string",
                        "material":"string",
                        "color":"string",
                        "size":"string",
                        "manufacturer":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "fashionItems":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "type":"string",
                        "material":"string",
                        "size":"string",
                        "manufacturer":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "sleepingGear":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "material":"string",
                        "color":"string",
                        "size":"string",
                        "components":"string",
                        "manufacturer":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "furniture":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "certificationType":"string",
                        "color":"string",
                        "components":"string",
                        "material":"string",
                        "manufacturer":"string",
                        "importer":"string",
                        "producer":"string",
                        "size":"string",
                        "installedCharge":"string",
                        "warrantyPolicy":"string",
                        "refurb":"string",
                        "afterServiceDirector":"string"
                    },
                    "imageAppliances":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "energyEfficiencyRating":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "additionalCost":"string",
                        "displaySpecification":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    
                    "homeAppliances":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string","modelName":"string",
                        "certificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "energyEfficiencyRating":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "additionalCost":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "seasonAppliances":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "energyEfficiencyRating":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "area":"string",
                        "installedCharge":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "officeAppliances":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "energyEfficiencyRating":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "weight":"string",
                        "specification":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "opticsAppliances":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "weight":"string",
                        "specification":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "microElectronics":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "weight":"string",
                        "specification":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "navigation":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "weight":"string",
                        "specification":"string",
                        "updateCost":"string",
                        "freeCostPeriod":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "carArticles":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "certificationType":"string",
                        "caution":"string",
                        "manufacturer":"string",
                        "size":"string",
                        "applyModel":"string",
                        "warrantyPolicy":"string",
                        "roadWorthyCertification":"string",
                        "afterServiceDirector":"string"
                    },
                    "medicalAppliances":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "licenceNo":"string",
                        "advertisingCertificationType":"string",
                        "ratedVoltage":"string",
                        "powerConsumption":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "purpose":"string",
                        "usage":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "kitchenUtensils":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "material":"string",
                        "component":"string",
                        "size":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "producer":"string",
                        "importDeclaration":True,
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "cosmetic":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "capacity":"string",
                        "specification":"string",
                        "expirationDateType":"CALENDER",
                        "expirationDate":"string",
                        "expirationDateText":"string",
                        "usage":"string",
                        "manufacturer":"string",
                        "producer":"string",
                        "distributor":"string",
                        "customizedDistributor":"string",
                        "mainIngredient":"string",
                        "certificationType":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "jewellery":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "material":"string",
                        "purity":"string",
                        "bandMaterial":"string",
                        "weight":"string",
                        "manufacturer":"string",
                        "producer":"string",
                        "size":"string",
                        "caution":"string",
                        "specification":"string",
                        "provideWarranty":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "food":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "foodItem":"string",
                        "weight":"string",
                        "amount":"string",
                        "size":"string",
                        "packDateType":"CALENDER",
                        "packDate":"2023-01-03",
                        "packDateText":"string",
                        "expirationDateType":"CALENDER",
                        "expirationDate":"2023-01-03",
                        "expirationDateText":"string",
                        "consumptionDateType":"CALENDER",
                        "consumptionDate":"2023-01-03",
                        "consumptionDateText":"string",
                        "producer":"string",
                        "relevantLawContent":"string",
                        "productComposition":"string",
                        "keep":"string",
                        "adCaution":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "generalFood":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "productName":"string",
                        "foodType":"string",
                        "producer":"string",
                        "location":"string",
                        "packDateType":"CALENDER",
                        "packDate":"2023-01-03",
                        "packDateText":"string",
                        "expirationDateType":"CALENDER",
                        "expirationDate":"2023-01-03",
                        "expirationDateText":"string",
                        "consumptionDateType":"CALENDER",
                        "consumptionDate":"2023-01-03",
                        "consumptionDateText":"string",
                        "weight":"string","amount":"string",
                        "ingredients":"string",
                        "nutritionFacts":"string",
                        "geneticallyModified":True,
                        "consumerSafetyCaution":"string",
                        "importDeclarationCheck":True,
                        "customerServicePhoneNumber":"string"
                    },
                    "dietFood":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "productName":"string",
                        "foodType":"string",
                        "producer":"string",
                        "location":"string",
                        "packDateType":"CALENDER",
                        "packDate":"2023-01-03",
                        "packDateText":"string",
                        "expirationDateType":"CALENDER",
                        "expirationDate":"2023-01-03",
                        "expirationDateText":"string",
                        "consumptionDateType":"CALENDER",
                        "consumptionDate":"2023-01-03",
                        "consumptionDateText":"string",
                        "storageMethod":"string",
                        "weight":"string",
                        "amount":"string",
                        "ingredients":"string",
                        "nutritionFacts":"string",
                        "specification":"string",
                        "cautionAndSideEffect":"string",
                        "nonMedicinalUsesMessage":"string",
                        "geneticallyModified":True,
                        "importDeclarationCheck":True,
                        "consumerSafetyCaution":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "kids":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "size":"string",
                        "weight":"string",
                        "color":"string",
                        "material":"string",
                        "recommendedAge":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "caution":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string",
                        "numberLimit":"string"
                    },
                    "musicalInstrument":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "size":"string",
                        "color":"string",
                        "material":"string",
                        "components":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "detailContent":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "sportsEquipment":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "size":"string",
                        "weight":"string",
                        "color":"string",
                        "material":"string",
                        "components":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "detailContent":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "books":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "title":"string",
                        "author":"string",
                        "publisher":"string",
                        "size":"string",
                        "pages":"string",
                        "components":"string",
                        "publishDateType":"CALENDER",
                        "publishDate":"2023-01-03",
                        "publishDateText":"string",
                        "description":"string"
                    },
                    "rentalEtc":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "ownershipTransferCondition":"string",
                        "payingForLossOrDamage":"string",
                        "refundPolicyForCancel":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "digitalContents":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "producer":"string",
                        "termsOfUse":"string",
                        "usePeriod":"string",
                        "medium":"string",
                        "requirement":"string",
                        "cancelationPolicy":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "giftCard":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "issuer":"string",
                        "periodStartDate":"2023-01-03",
                        "periodEndDate":"2023-01-03",
                        "periodDays":0,
                        "termsOfUse":"string",
                        "useStorePlace":"string",
                        "useStoreAddressId":0,
                        "useStoreUrl":"string",
                        "refundPolicy":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "mobileCoupon":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "issuer":"string",
                        "usableCondition":"string",
                        "usableStore":"string",
                        "cancelationPolicy":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "movieShow":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "sponsor":"string",
                        "actor":"string",
                        "rating":"string",
                        "showTime":"string",
                        "showPlace":"string",
                        "cancelationCondition":"string",
                        "cancelationPolicy":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "etcService":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "serviceProvider":"string",
                        "certificateDetails":"string",
                        "usableCondition":"string",
                        "cancelationStandard":"string",
                        "cancelationPolicy":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "biochemistry":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "productName":"string",
                        "dosageForm":"string",
                        "packDateType":"CALENDER",
                        "packDate":"string",
                        "packDateText":"string",
                        "expirationDateType":"CALENDER",
                        "expirationDate":"string",
                        "expirationDateText":"string",
                        "weight":"string",
                        "effect":"string",
                        "importer":"string",
                        "producer":"string",
                        "manufacturer":"string",
                        "childProtection":"string",
                        "chemicals":"string",
                        "caution":"string",
                        "safeCriterionNo":"string",
                        "customerServicePhoneNumber":"string"
                    },
                    "biocidal":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "productName":"string",
                        "weight":"string",
                        "effect":"string",
                        "rangeOfUse":"string",
                        "importer":"string",
                        "producer":"string",
                        "manufacturer":"string",
                        "childProtection":"string",
                        "harmfulChemicalSubstance":"string",
                        "maleficence":"string",
                        "caution":"string",
                        "approvalNumber":"string",
                        "customerServicePhoneNumber":"string",
                        "expirationDateType":"CALENDER",
                        "expirationDate":"string",
                        "expirationDateText":"string"
                    },
                    "cellPhone":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificationType":"string",
                        "releaseDateType":"CALENDER",
                        "releaseDate":"string",
                        "releaseDateText":"string",
                        "manufacturer":"string",
                        "importer":"string",
                        "producer":"string",
                        "size":"string",
                        "weight":"string",
                        "telecomType":"string",
                        "joinProcess":"string",
                        "extraBurden":"string",
                        "specification":"string",
                        "warrantyPolicy":"string",
                        "afterServiceDirector":"string"
                    },
                    "etc":
                    {
                        "returnCostReason":"string",
                        "noRefundReason":"string",
                        "qualityAssuranceStandard":"string",
                        "compensationProcedure":"string",
                        "troubleShootingContents":"string",
                        "itemName":"string",
                        "modelName":"string",
                        "certificateDetails":"string",
                        "manufacturer":"string",
                        "afterServiceDirector":"string",
                        "customerServicePhoneNumber":"string"
                    }
                },
                "productAttributes":
                [
                    {
                        "attributeSeq":0,
                        "attributeValueSeq":0,
                        "attributeRealValue":"string",
                        "attributeRealValueUnitCode":"string"
                    }
                ],
                "cultureCostIncomeDeductionYn":True,
                "customProductYn":True,
                "itselfProductionProductYn":True,
                "brandCertificationYn":True,
                "seoInfo":
                {
                    "pageTitle":"string",
                    "metaDescription":"string",
                    "sellerTags":
                    [
                        {
                            "code":0,
                            "text":"string"
                        }
                    ]
                }
        },
            "customerBenefit":
            {
                "immediateDiscountPolicy":
                {
                    "discountMethod":
                    {
                        "value":0,
                        "unitType":"PERCENT",
                        "startDate":"2023-01-03T14:32:30Z",
                        "endDate":"2023-01-03T14:32:30Z"
                    },
                    "mobileDiscountMethod":
                    {
                        "value":0,
                        "unitType":"PERCENT",
                        "startDate":"2023-01-03T14:32:30Z",
                        "endDate":"2023-01-03T14:32:30Z"
                    }
                },
                "purchasePointPolicy":
                {
                    "value":0,
                    "unitType":"PERCENT",
                    "startDate":"2023-01-03",
                    "endDate":"2023-01-03"
                },
                "reviewPointPolicy":
                {
                    "textReviewPoint":0,
                    "photoVideoReviewPoint":0,
                    "afterUseTextReviewPoint":0,
                    "afterUsePhotoVideoReviewPoint":0,
                    "storeMemberReviewPoint":0,
                    "startDate":"2023-01-03",
                    "endDate":"2023-01-03"
                },
                "freeInterestPolicy":
                {
                    "value":0,
                    "startDate":"2023-01-03",
                    "endDate":"2023-01-03"
                },
                "giftPolicy":
                {
                    "presentContent":"string"
                },
                "multiPurchaseDiscountPolicy":
                {
                    "discountMethod":
                    {
                        "value":0,
                        "unitType":"PERCENT",
                        "startDate":"2023-01-03",
                        "endDate":"2023-01-03"
                    },
                    "orderValue":0,
                    "orderValueUnitType":"PERCENT"
                }
            }
        },
        
        "smartstoreChannelProduct":
        {
            "channelProductName":"string",
            "storeKeepExclusiveProduct":True,
            "naverShoppingRegistration":True,
            "bbsSeq":0,
            "channelProductDisplayStatusType":"WAIT"
        },
        
        "windowChannelProduct":
        {
            "channelProductName":"string",
            "storeKeepExclusiveProduct":False,
            "naverShoppingRegistration":True,
            "bbsSeq":0,
            "channelNo":channelNo,
            "best":False
            }
    }
"""
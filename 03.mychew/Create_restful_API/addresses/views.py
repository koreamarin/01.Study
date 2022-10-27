import re
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import AddressesSerializer
from .models import Addresses

# Create your views here.
@csrf_exempt
def address_list(request) :
    if request.method == 'GET' :
        data = Addresses.objects.all()
        serializer = AddressesSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST' :                             
        data = JSONParser().parse(request)                      # POST로 받은 JSON형식 딕셔너리 데이터를
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def address(request, pk) :
    try:
        obj = Addresses.objects.get(pk=pk)                      # Addresses 모델에서 pk(primary key)와 url에서 받은 pk값이 똑같은 테이블을 obj에 넣는다.
    except Addresses.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET' :
        serializer = AddressesSerializer(obj)                   # obj를 rest api에서 사용하는 직렬(serial)형태, 즉, json형태로 변환해줌.
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)        # request로 받은 data와 model에 저장되어 있는 obj을 serializer가 받는다.
        if serializer.is_valid():                               # is_valid는 형식이 적당한지 판별하는 함수이다. 모든 형식이 적당하다면 True를, 형식이 다르다면 False를 return한다.
            serializer.save()                                   # 형식이 적당하다면 serializer를 저장한다.
            return JsonResponse(serializer.data, status=201)    
        return JsonResponse(serializer.errors, status=400)        

    elif request.method == 'DELETE' :
        obj.delete()                                            # obj를 삭제한다.
        return HttpResponse(status=204)

@csrf_exempt
def login(request) :
        
    if request.method == 'POST' :
        data = JSONParser().parse(request)              # request로 받은 JSON을 JSONParser로 읽어서 data에 저장 함. 변수 data에 저장된 데이터는 딕셔너리 형태임. JSONParser를 사용하는 이유는 인코딩형식이 달라서 일것으로 추측.
        search_name = data['name']                      # 변수 data에서 Key인 name의 Value만을 출력.
        print(search_name)
        obj = Addresses.objects.get(name=search_name)           # POST형식으로 받은 request에서 name의 value 값과 같은 name의 테이블을 model에서 찾아 obj에 넣는다. 
        print(obj.phone_number)                         # model에서 찾은 name의 value값과 같은 테이블에서 phone_number을 print로 출력한다.

        if data['phone_number'] == obj.phone_number :       # request에서 post형식으로 받아 data에 넘긴 phone_number와 모델에서 얻은 obj의 phone_number가 같다면 아래 문장을 실행.
            return HttpResponse("<div>로그인성공</div>",status=200)
        else :
            return HttpResponse(status=400)
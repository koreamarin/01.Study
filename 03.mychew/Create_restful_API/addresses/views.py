import re
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import AddressesSerializer
from .models import Addresses
from django.contrib.auth.models import User                 # 로그인 기능을 만들 때 
from django.contrib.auth import authenticate

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
        print(data)
        print()
        print(serializer)
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
    if request.method == 'POST':
        request_post = request.POST
        login_id = request_post['userid']
        login_pw = request_post['userpw']

        result = authenticate(username=login_id, password=login_pw)     # 이 함수에 id와 pw를 넣어서 로그인에 성공하면 id를 반환, 로그인에 실패하면 None을 반환한다.
    
        print(f'result = {result}')
        
        if result :
            print("로그인성공")                                         # result에 값이 들어가서 True로 판단되면 로그인성공 메세지출력
            return HttpResponse("<div>로그인성공</div>",status=200)     
        else :                                                          # result에 값이 None이 들어가 False로 판단되면 로그인실패 메세지출력
            print("로그인실패") 
            return HttpResponse(status=401)

    elif request.method == 'GET' :
        return render(request, 'addresses/login.html')              # setting에 보면 TEMPLATES의 'DIRS': [os.path.join(BASE_DIR,'templates')]에다가 템플릿 기본경로를 설정해둬서 이 문장에서 templates 경로를 넣지 않았다.

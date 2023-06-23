import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError, ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user).data
        return Response(serializer)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ValidationError("Password is required")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)     # 비밀번호를 암호화하여 저장한다. 이때 암호화된 비밀번호는 DB에 저장된다. user.password=password는 비밀번호를 암호화하지 않고 저장되는데 이 방식을 사용하면 안된다.
            user.save()                     # user.set_password(password)를 사용하여 비밀번호를 암호화하여 다시 저장한다.
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class PublicUser(APIView):


    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
    
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]


    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):   # 이전의 비밀번호가 맞다면 True를 반환한다.
            user.set_password(new_password)     # 새로운 비밀번호를 저장한다.
            user.save()                         # 저장한다.
            return Response(status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)   # authenticate는 username과 password를 받아서 해당 유저가 있는지 확인하고, 있으면 해당 유저를 반환한다.
        if user:
            login(request, user)    # login은 authenticate를 통해 반환된 user를 request에 저장한다. 이제 request.user에 user 정보가 들어가 있어 인증이 가능하다.
            return Response({"ok":"Welcome"})
        else :
            return Response({"error": "Wrong username or password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)     # logout은 request에 저장된 user를 지운다.
        return Response({"ok":"Bye!"})


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)   # authenticate는 username과 password를 받아서 해당 유저가 있는지 확인하고, 있으면 해당 유저를 반환한다.
        if user:
            # jwt.encode는 토큰을 생성한다. 첫번째 인자는 토큰에 들어갈 내용이다.
            # 두번째 인자는 시크릿키이다.시크릿키는 settings.py에 저장되어 있는 SECRET_KEY를 사용하였다.
            # 세번쨰 인자는 알고리즘이다. 알고리즘은 HS256을 사용하였다. 토큰을 암호화할 때 해당 알고리즘을 사용한다.
            token = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response({"token":token})
        else:
            return Response({"error": "Wrong username or password"})
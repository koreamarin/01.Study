import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


# 인증 클래스를 만들기 위해서는 BaseAuthentication을 상속받아야 한다.
class TrustMeBroAuthentication(BaseAuthentication):
    # 인증과정을 거친 후에 인증에 성공하면 (user, token)의 형태로 반환하기만 하면 된다. 그럼 인증 성공이다.
    # 함수명은 반드시 authenticate여야 한다.
    def authenticate(self, request):
        username = request.headers.get("Trust-Me")
        if not username:
            return None     # 유저정보가 없으면 None을 반환하며 view를 계속 실행한다.
        try:
            user = User.objects.get(username=username)
            # (user, token)의 형태로 반환해야 한다. 튜플 형태로 반환하는 것이 규칙이다.
            # 여기에서 user는 views.py에서 흔히 사용되는 request.user이다.
            # request.user는 클라이언트가 보낸것이 아닌, 서버에서 인증을 거친 후에 반환하는 값이다.
            return (user, None)     # 유저정보를 반환 후 view를 계속 실행한다.
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No  user {username}")  # 인증에 실패하면 AuthenticationFailed를 발생시킨다.


class JWTAuthentication(BaseAuthentication):
    # 인증과정을 거친 후에 인증에 성공하면 (user, token)의 형태로 반환하기만 하면 된다. 그럼 인증 성공이다.
    # 함수명은 반드시 authenticate여야 한다.
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token :
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get('pk')
        if not pk:
            raise AuthenticationFailed("Invalid token")
        try :
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")

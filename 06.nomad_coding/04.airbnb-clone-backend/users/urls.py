from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token    # rest_framework의 인증방식중 하나인 TokenAuthentication을 사용하기 위해 추가해준다.
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    # 이 URL에 POST요청으로 username과 password를 보내면 토큰을 반환한다.
    # 이 토큰은 Authorization헤더에 담아서 서버로 보내는 방식으로 인증을 한다.
    # 사용자 정보를 보내는 것이 아니라 토큰을 보내는 것으로 인증을 한다.
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogIn.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    
    
]
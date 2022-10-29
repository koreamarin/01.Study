from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from addresses import views
from django.contrib import admin                            # 관리자페이지 접속할 수 있게 해주는 라이브러리


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('addresses', views.address_list),
    path('addresses/<int:pk>', views.address),
    path('login', views.login),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin', admin.site.urls)
]


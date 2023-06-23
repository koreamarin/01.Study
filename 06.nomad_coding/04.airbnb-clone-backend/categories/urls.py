from django.urls import path
from . import views

urlpatterns = [
    # views.py 에서 class를 가져오려면 as_view()를 붙여줘야 한다.
    # as_view()는 요청이 get이면 클래스 내의 get 함수를 실행하고
    # 요청이 post이면 클래스 내의 post 함수를 실행한다.
    # path("", views.categories), # 함수를 이용하여 구현하기
    # path("<int:pk>/", views.category),    # 함수를 이용하여 구현하기
    #
    # path("", views.Categories.as_view()), # 클래스를 이용하여 구현하기
    # path("<int:pk>/", views.CategoryDetail.as_view()),    # 클래스를 이용하여 구현하기
    #
    # 뷰셋을 이용하여 구현하기
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>/",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]

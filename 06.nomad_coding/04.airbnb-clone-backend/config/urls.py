from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
    path("api/v1/users/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # 이미지를 요청할 URL과 장고가 이미지를 찾을 경로를 설정해준것.
# 즉, user가 MEDIA_URL로 요청을 보내면 장고는 MEDIA_ROOT폴더에서 같은 이름의 파일을 찾아서 응답해준다.

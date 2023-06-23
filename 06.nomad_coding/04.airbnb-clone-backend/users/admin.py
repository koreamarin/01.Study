from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # # 해당 방식으로 사용하면 관리자페이지에서 섹션이 없는 각 필드 수정란이 나타난다.
    # field= ("username", "password", "name", "email", "is_host")

    # 해당 방식 fields가아닌 fieldsets을 사용하면 섹션을 나눠서 보여줄 수 있다.
    # 섹션 name을 None으로 지정하면 해당 섹션의 이름이 나타나지 않는다.
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                    "language",
                    "currency",
                ),
                "classes": ("wide",),  # 해당 섹션을 넓게 보여준다.
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),  # 해당 섹션을 접을 수 있게 한다. 섹션 옆에 (보기)가 나타나며 토글처럼 접을 수 있다.
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "name",
        "is_host",
        "is_staff",
    )

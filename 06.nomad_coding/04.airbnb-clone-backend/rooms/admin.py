from django.contrib import admin
from .models import Room, Amenity


# admin 페이지에 체크박스에 선택한 object에 대해 action을 취할 수 있도록 해준다.
# 예를들어 선택한 object의 price를 0으로 만들거나, 삭제하는 등의 작업을 할 수 있다.
# action은 model_admin, request, queryset 총 3개의 매개변수가 필요하다.
# model_admin은 class로부터 인자를 받는다.
# request는 user의 정보를 가지고 있다. 유저가 권한을 가지는지 확인하기 위함으로 사용할 수 있다.
# queryset은 선택된 모든 object를 가지고 있다.
# 아래는 모든 object의 price를 0으로 만드는 action이고, 액션 텍스트가 Set all prices to zero로 나온다.
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, queryset):
    for room in queryset:
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)  # 해당 admin 페이지에 액션을 추가할 수 있다.

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )

    list_filter = (  # 필터 옵션, Room의 데이터를 볼 때 필터 옵션을 줘서 볼 수 있음
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    # admin 페이지의 목록에서 검색을 할 수 있도록 해준다. 검색되는 필드는 name과 price이다.
    search_fields = (
        # "^name",  # "^name"으로 하면 name으로 시작하는 것만 검색된다.
        # "=price",  # "=price"로 하면 정확히 일치하는 것만 검색된다.
        "owner__username",  # owner의 username으로 검색할 수 있다. ^나 =가 없으면 일부분만 검색해도 검색된다.
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (  # 이것을 추가하면 Amenity의 상세페이지에서 created_at, updated_at을 볼 수 있다. 하지만 읽기모드이므로 수정은 불가능하다.
        "created_at",
        "updated_at",
    )

from typing import Any, Optional
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review


# 필터 목록을 직접 추가하기 위해 사용되는 클래스이다.
# list_filter에 추가된 필터는 admin페이지에서 필터 목록으로 나타난다.


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"  # title은 필터 이름으로 나타난다.

    parameter_name = "potato"  # 필터를 걸 때 사용되는 파라미터 이름이다. ex) ?potato=good

    def lookups(self, request, model_admin):  # admin의 필터 목록에 나타날 내용을 정의하는 함수.
        return [  # 리스트+ 튜플의 형태로 반환해야 한다.
            ("good", "Good"),  # 필터 목록에 나타날 이름과 실제 필터링에 사용될 이름을 정의한다.
            ("great", "Great"),
            ("super", "Super"),
        ]

    def queryset(self, request, reviews):  # admin에서 필터를 선택하면 어떤 인자를 return하여 보여줄 것인지 정하는 함수.
        word = self.value()  # self.value()는 위의 lookups에서 정의한 이름을 반환한다. admin 페이지에서 선택한 필터의 이름이다.
        if word:
            return reviews.filter(
                payload__contains=word
            )  # 3번째 인자인 reviews에는 reviews의 queryset이 들어있다. 해당 쿼리셋에 admin에서 받은 필터value로 필터를 건 것이다.
        else:
            return reviews


class RatingFilter(admin.SimpleListFilter):
    title = "Filter by rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word == "good":
            return reviews.filter(rating__gte=4)
        elif word == "bad":
            return reviews.filter(rating__lt=4)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",  # str 함수를 display할 수 있다.
        "payload",
    )
    list_filter = (
        WordFilter,
        RatingFilter,
        "rating",
        "user__is_host",  # 외래키로도 필터를 줄 수 있다.
        "room__category",
        "room__pet_friendly",
    )

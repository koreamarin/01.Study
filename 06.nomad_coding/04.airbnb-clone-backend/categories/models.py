from django.db import models
from common.models import CommonModel


class Category(CommonModel):

    """Room or Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return f"{self.kind.title()}: {self.name}"  # title을 쓰면 맨 앞 글자만 대문자로 바꿔줌

    class Meta:
        verbose_name_plural = (
            "Categiries"  # admin에서 복수형을 따로 표시해주지 않으면 Amenitys로 표시되는데 그걸 Amenities로 바꿔줌
        )

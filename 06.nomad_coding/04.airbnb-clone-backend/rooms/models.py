from django.db import models
from common.models import CommonModel


class Room(CommonModel):

    """Room Model Definition"""

    class RoomkindChoices(models.TextChoices):
        ENTIRE_PLACE = "entire_place", "Entire Place"
        PRIVATE_ROOM = "private_room", "Private Room"
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=80,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=80,
        choices=RoomkindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):  # values만을 꺼내와서 최적화를 할 수 있다.
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):

    """Amenity Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = (
            "Amenities"  # admin에서 복수형을 따로 표시해주지 않으면 Amenitys로 표시되는데 그걸 Amenities로 바꿔줌
        )

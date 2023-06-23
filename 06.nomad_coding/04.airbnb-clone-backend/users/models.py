from django.db import models
from django.contrib.auth.models import AbstractUser


# 만약 models.Model을 상속받으면 모든 필드를 내가 다 만들어야한다.
# AbstractUser를 상속받으면 장고가 기존에 구현해 놓았던 User, password 등을 사용할 수 있다.
# 따라서 AbstractUser를 상속받아 장고가 구현에 놓은 것들에 필요한 것들만 확장하는 방식으로 구현한 모델이다.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        KRW = ("won", "Korean Won")
        USD = ("usd", "Dollar")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.URLField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
        verbose_name="Is Host",
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )

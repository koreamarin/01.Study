from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Addresses(models.Model) :         # 모델, 모델명 선언 할 클래스 생성.
    name = models.CharField(max_length=10, blank=False, default='류지원')
    phone_number = models.CharField(max_length = 13)
    address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
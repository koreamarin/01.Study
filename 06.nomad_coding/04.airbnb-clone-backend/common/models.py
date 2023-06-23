from django.db import models


# 이런 모델을 abstract model이라고 한다.
# abstract model은 데이터베이스에 나타나지 않는다.
# 이 모델을 상속받는 모델들은 이 모델의 필드들을 상속받아 사용할 수 있다.
class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

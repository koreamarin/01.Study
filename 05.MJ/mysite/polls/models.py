import datetime

from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model) :
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):              # Question.objects.all()등의 API명령어를 통해 model을 호출할 때 모델안에 든 데이터를 출력하기 위한 함수.
        return self.question_text

    def was_published_recently(self):                                           # 생성일이 최근이면 True를, 최근이 아니면 False를 호출하는 함수.
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)            # Choicd 모델의 외래키는 question으로 명시해줌. question은 Question에 관계되었다는 것을 명시해줌. on_delete=models.CASCADE의 뜻은 Chioce에 관계되어있는 Question이 삭제되면 관계되어있는 Choice의 모델도 삭제가 자동으로 되게끔 명시해 준 것이다.
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
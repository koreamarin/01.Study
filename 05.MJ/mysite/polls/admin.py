from django.contrib import admin

from .models import Question, Choice

# Register your models here.
# 1
# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 1

# 2
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1           # medel의 데이터를 보여주는 것 이외에 1개의 추가적인 창을 더 나타내어줌.


# # 1
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

# 2
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [                           # 상세보기에서 필드별로 나타내어줌. 맨 앞 인자는 필드네임, 두번째 인자의 딕셔너리에 value 값에는 list가 들어가는데 나타내어줄 모델의 데이터를 명시해주면 됨.
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]                # 인라인 방식
    list_display = ('question_text', 'pub_date')    # TABLE(MODEL)의 리스트 창에서 Question TEXT 뿐만 아니라 DATE PUBLISHED까지 보여주는 명령어.


# admin.site.register(Question)
# admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)

from django.apps import AppConfig


class DirectMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "direct_messages"
    verbose_name = "Direct Messages"  # admin페이지의 목록에 나타나는 이름을 변경하기 위해 사용

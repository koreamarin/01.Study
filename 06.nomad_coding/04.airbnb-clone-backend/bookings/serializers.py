from django.utils import timezone

from rest_framework import serializers
from .models import Booking

class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
            )
        

    # check_in의 값이 유효한지 검사하는 함수. 함수명은 validate_필드명으로 작성한다.
    # check_in이 들어오면 자동으로 실행되고, check_in의 값이 유호한지 검사해주는 함수이다.
    # value는 check_in의 값이다.
    # check_in의 값이 유효하면 value를 return 하고, 유효하지 않으면 에러를 발생시킨다.
    def validate_check_in(self, value):     # value는 check_in의 값이다.
        now = timezone.localtime(timezone.now()).date()     # 현재 시간을 가져오되, localtime을 적용하여 현재위치를 기준으로 시간을 적용하여 가져온다. 그리고 날짜만 가져온다.
        if now > value:
            raise serializers.ValidationError("Can't check in the past")
        return value
    
    def validate_check_out(self, value):     # value는 check_in의 값이다.
        now = timezone.localtime(timezone.now()).date()     # 현재 시간을 가져오되, localtime을 적용하여 현재위치를 기준으로 시간을 적용하여 가져온다. 그리고 날짜만 가져온다.
        if now > value:
            raise serializers.ValidationError("Can't check out the past")
        return value

    def validate(self, data):
        if data['check_out'] < data['check_in']:
            raise serializers.ValidationError("Check in should be smaller then check out.")
        
        if Booking.objects.filter(
            check_in__lte=data['check_out'],
            check_out__gte=data['check_in'],
        ).exists() :
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        return data





class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
            )

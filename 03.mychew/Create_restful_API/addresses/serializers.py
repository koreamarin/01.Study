from rest_framework import serializers
from .models import Addresses

class AddressesSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Addresses                        # Serializer을 사용할 모델로 Addresses 모델을 사용할 것임을 명시. Serializer는 응답으로 보낼 데이터의 형태를 정해주는 기능을 함.
        fields = ['name', 'phone_number', 'address', 'created']      # 모델의 모든 요소를 명시할 필요는 없음.
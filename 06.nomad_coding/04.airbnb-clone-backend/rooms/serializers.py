from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    # 이렇게 fields명 변수에 serializer을 넣으면 커스텀된 serializer를 사용하여 원하는 필드만 가져올 수 있다.
    # read_only=True을 써 놓으면 내보내기만 가능하고, 받기는 제외할 수 있다.
    # room을 올리는 이가 room의 주인인 user을 수정할 수 있는 권한을 주면 안되므로 read_only=True를 써준다.
    owner = TinyUserSerializer(read_only=True)
    # 가져올 필드가 여러개일 경우 many=True를 사용한다.
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(read_only=True)

    # SerializerMethodField()는 연결된 함수를 실행시켜서 그 함수의 return 을 받아온다.
    # 이 함수는 get_필드명(self, instance) 형태로 작성한다.
    # 아래 변수의 연결된 함수는 get_rating(self, rooms) 이다.
    # rooms는 Room 모델의 인스턴스이다.
    rating = serializers.SerializerMethodField()   
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)


    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1   # depth = 1 은 foreign key를 1단계 까지만 보여준다는 의미. 모든 오브젝트를 다 가져와버리므로 잘 사용하지는 않는다.


    # SerializerMethodField()는 연결된 함수를 실행시켜서 그 함수의 return 을 받아온다.
    # 이 함수는 get_필드명(self, instance) 형태로 작성한다.
    # 아래 변수의 연결된 함수는 get_rating(self, rooms) 이다.
    # rooms는 Room 모델의 인스턴스이다.
    def get_rating(self, room): # 2번쨰 인자에는 room 모델이 들어온다.
        return room.rating()

    def get_is_owner(self, room):   # 이 요청을 한 request.user와 serializer에 들어간 room.owner가 같은지 확인하는 함수
        request = self.context['request']
        return room.owner == request.user   # 요청 user와 room의 owner가 같으면 True, 다르면 False를 return 한다.

    # room에 좋아요를 눌렀는지 확인하는 함수
    def get_is_liked(self, room):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists() # 존재여부를 확인

class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room): # 2번쨰 인자에는 room 모델이 들어온다.
        return room.rating()
    
    def get_is_owner(self, room):   # 이 요청을 한 request.user와 serializer에 들어간 room.owner가 같은지 확인하는 함수
        request = self.context['request']
        return room.owner == request.user   # 요청 user와 room의 owner가 같으면 True, 다르면 False를 return 한다.

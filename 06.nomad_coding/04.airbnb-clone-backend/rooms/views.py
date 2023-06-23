from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    # IsAuthenticatedOrReadOnly는 인증이 되어있지 않으면 GET 요청만 가능하고, POST, PUT, DELETE 요청은 불가능하다.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        # 아래에서 자주 나오는 request.user 모델은 클라이언트로부터 user모델은 클라이언트가 로그인한후 django에서 클라이언트로 보냈던 user모델을 다시 받은것이다.
        # if not request.user.is_authenticated:  # request를 보낸 유저가 인증된 유저인지 확인. 세션을 기반으로 로그인된 유저인지 확인.
        # raise NotAuthenticated            # 인증된 유저가 아닐 시 NotAuthenticated 에러를 발생시킨다.
        serializer = RoomDetailSerializer(
            data=request.data
        )  # request.data는 request.user와 다르게 클라이언트가 직접 생성하여 보낸 데이터이다.
        if serializer.is_valid():  # serializer가 유효한 데이터인지 확인
            # 유저가 보낸 request.data에 category가 있는지 확인.
            category_pk = request.data.get("category")
            if not category_pk:  # 유저가 보낸 category가 없다면 실행. 에러 메세지를 반환.
                raise ParseError(
                    "Category is required"
                )  # 유저가 잘못된 데이터를 보냈을 경우 발생하는 에러. 괄호안에는 에러내용을 적을 수 있다.
            try:  # 유저가 보낸 category가 있었지만 pk가 존재하지 않을 경우 오류가 발생하므로 try, except를 추가.
                category = Category.objects.get(pk=category_pk)
                if (
                    category.kind == Category.CategoryKindChoices.EXPERIENCES
                ):  # 유저가 보낸 category의 kind가 EXPERIENCES인지 확인. experinces는 room에 추가할 수 없다.
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            # owner를 request.user로 설정해준다.
            # owner를 설정해주지 않으면, request를 보낸 유저가 room의 주인이 아니게 된다.
            # save()의 매개변수로 owner를 넣어주면, create()의 매개변수 validated_data로 owner를 추가로 넣어주는 것이다.
            # room은 owner, amenities, category를 read_only=True하였는데,
            # owner은 model에서 필수 필드로 설정하였므로, owner를 넣어주지 않으면 에러가 발생한다.
            # 결론은 read_only된 필드에 추가로 필드데이터로 구성된 인자를 넣어주고 싶다면 save함수에 매개변수로 넣어주면 된다.
            # 즉 save함수에 넣은 매개변수는 클라이언트로 부터 받는 데이터는 맞지만
            # 클라이언트가 원해서 넣는 데이터가 아니라 클라이언트 정보로부터 추출된 데이터이므로 조작할 수 없는 데이터이다.
            # 찐 결론은 클라이언트가 로그인한 세션 정보기반으로 유저정보를 저장해버리는 것이다.

            # transaction.atomic()은 데이터베이스에 저장할때, 에러가 발생하면 저장하지 않는다.
            # transaction.atomic() 안에 있는 코드들은 즉시 실행되지 않으며, 어떤 오류도 발견되지 않았을떄 실행된다.
            # transaction.atomic() 안에 try, except 구문이 있으면 error를 transacton이 인지하지 못하므로 안에 사용하지 않는다.
            # 하지만 사용자도 오류를 알아야하므로 transaction.atomic() 바깥에 try, except를 사용하여 오류 구문을 출력한다.
            # 그렇게 사용하면 오류 발생시 transaction안에 있는 코드들도 실행되지 않았고, 오류가 발견되었으므로 except 구문이 실행된다.
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    # room과 amenities는 다대다 관계이므로, add, remove등의 함수를 사용하여 room에 amenities를 추가, 삭제해주는 방식을 사용한다.
                    # 위에서 save후에 room object를 반환받았으므로, 그 room object에 amenities를 추가해준다.
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        # if not request.user.is_authenticated :    # IsAuthenticatedOrReadOnly를 사용하므로 주석처리
        #     raise NotAuthenticated

        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            # 카테고리
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    room.amenities.clear()
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        # if not request.user.is_authenticated :            # IsAuthenticatedOrReadOnly를 사용하므로 주석처리
        #     raise NotAuthenticated

        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = page * page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            # 슬라이싱 구조는 [start, end]으로 되어있다.
            # 리스트에서는 모든 리스트를 가져온 뒤에 슬라이싱이 실행되지만
            # 장고에서 쿼리셋을 슬라이싱 하는 경우에는 장고가 offset과 limit에 대한 정보를 포함하여
            # 데이터베이스에 정보를 요청하여 쿼리를 가져온다.
            # 예를 들어 쿼리에 [5:12]이 붙이있는 경우에는
            # 데이터베이스에는 offset=5, limit=7로 요청하여 5번째부터 12번째까지의 데이터를 가져온다.
            # 따라서 모든 데이터를 가져오지 않고, 필요한 데이터만 가져오므로 성능이 향상된다.
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)

        if room.owner == request.user:
            raise PermissionDenied

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                room=room,
                user=request.user,
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = 5
        start = (page - 1) * page_size
        end = page * page_size

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        # if not request.user.is_authenticated :      # IsAuthenticatedOrReadOnly를 사용하므로 주석처리
        #     raise NotAuthenticated

        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied

        seriallizer = PhotoSerializer(data=request.data)
        if seriallizer.is_valid():
            photo = seriallizer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(seriallizer.errors)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,  # room에 대한 booking만 가져온다. experience는 가져오지 않는다.
            check_in__gt=now,  #  현재 날짜 이후의 예약만 가져온다.
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )

            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

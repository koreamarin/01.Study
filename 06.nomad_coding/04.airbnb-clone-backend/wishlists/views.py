from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):
    # Wishlists는 본인만이 볼 수 있기에 get 또한 인증이 필요하다. 그래서 IsAuthenticated를 사용한다.
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Wishlist.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(all_wishlists, many=True, context={"request": request})
        return Response(data=serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(data=serializer.data)

        else :
            return Response(serializer.errors)
        
class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)   # 유저 정보를 추가로 넣어 해당 유저의 위시리스트만 가져올 수 있도록 한다.
        except Wishlist.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, context={"request": request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist, context={"request": request})
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class WishlistToggle(APIView):

    permission_classes = [IsAuthenticated]

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)   # 유저 정보를 추가로 넣어 해당 유저의 위시리스트만 가져올 수 있도록 한다.
        except Wishlist.DoesNotExist:
            raise NotFound

    
    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    # wishlist에 room을 추가하거나 삭제하는 함수
    # wishlist에 room이 있으면 삭제, 없으면 추가
    def put(self, request, pk, room_pk):        
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if  wishlist.rooms.filter(pk=room_pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)

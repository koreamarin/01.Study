from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from .models import Photo


class PhotoDetail(APIView):

    # 자동으로 인증을 해주는 클래스
    # 인증이 되어있지 않으면 403 에러를 발생시킨다.
    # 이 기능을 사용하면 request.user.is_authenticated를 따로 사용하지 않아도
    # 유저인증을 자동으로 해주기 때문에 편리하다.
    # 대신 클래스 전체에 적용되기 때문에 주의해야한다.
    # rooms/view.py에서 IsAuthenticatedOrReadOnly를 사용하고 있는데
    # IsAuthenticatedOrReadOnly는 인증이 되어있지 않으면 읽기만 가능하다
    # 즉, 인증이 되어있지 않으면 GET 요청만 가능하고, POST, PUT, DELETE 요청은 불가능하다.
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user):
            return PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)
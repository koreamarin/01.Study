from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer

"""
# 첫번쨰 방법 : 함수를 이용하여 구현하기
@api_view(["GET", "POST"])  # GET과 POST를 넣어서 rest_framework의 api_view에서 get과 post 방식을 활성화시킨다.
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(instance=all_categories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            update_category = serializer.save()
            return Response(CategorySerializer(update_category).data)
        else:
            return Response(serializer.errors)

    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
"""

"""
# 두번째 방법 : 클래스를 이용하여 구현하기
# 아래 클래스는 위 categories 함수를 클래스로 만든 것이다. 훨씬 간편하게 만들 수 있다.
class Categories(APIView):
    def get(self, request):  # GET Request를 받으면 실행되는 함수이다.
        all_categories = Category.objects.all()
        # serializer에서 내보낼때에는 instace에 데이터를 넣어준다. 만약 리스트로 이루어진 여러개의 데이터를 보낼때에는 many=True를 넣어준다.
        serializer = CategorySerializer(instance=all_categories, many=True)
        return Response(serializer.data)

    def post(self, request):  # POST Request를 받으면 실행되는 함수이다.
        # 클라이언트로부터 데이터를 받을때에는 data에 데이터를 넣어준다.
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()를 하면 serializers.py안에 만든 create() 함수가 자동실행된다.
            # 만약 data만 있지않고 instance도 있으면 update() 함수가 실행된다.
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)  # 이렇게 하면 새로 만든 카테고리의 데이터를 보여준다.
        else:
            return Response(serializer.errors)



# 아래 클래스는 위 category 함수를 클래스로 만든 것이다. 훨씬 간편하게 만들 수 있다.
class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:  # 클라이언트가 잘못된 pk를 보내면 404에러를 보내준다.
            raise NotFound  # raise는 오류를 출력한다. 그리고 그 다음 모든 코드를 멈춘다.

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,  # partial=True를 넣어주면 부분적으로 수정할 수 있다.
            # 즉, data에 들어갈 데이터가 serializers에서 정의하는 모든 변수를 포함하지 않더라도
            # 변수가 부분적으로도 들어갈 수 있음을 허락하여 부분적인 수정이 가능하도록 해준다.
        )
        if serializer.is_valid():
            # 현재 serializer.save()는 instance와 data 매개변수 모두를 가졌으므로 update() 함수를 실행한다.
            update_category = serializer.save()
            return Response(CategorySerializer(update_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)

"""


# 세번째 방법 : ViewSet을 이용하여 구현하기. 단순 CRUD 방식. 커스텀이 가능하긴 하지만 CRUD 이외의 기능을 수행하기에는 적합하지 않다.
class CategoryViewSet(ModelViewSet):
    # 만약 readonly를 사용하고 싶다면 ModelViewSet 대신 viewsets.ReadOnlyModelViewSet을 사용하면 된다. 이는 list, retrieve만 사용가능하다.
    # ViewSet은 ModelViewSet을 상속받아서 만든다.
    # ModelViewSet은 list, create, retrieve, update, destroy를 자동으로 만들어준다.
    # list는 GET, create는 POST, 개별 오브젝트를 보여주는 retrieve는 GET, update와 partial_update는 PUT, destroy는 DELETE이다.
    # ViewSet은 2가지 property를 가진다. serializer_class와 queryset이다.
    # serializer_class는 어떤 serializer를 사용할지 정해주는 것이다.
    # queryset은 어떤 데이터를 사용할지 정해주는 것이다.
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

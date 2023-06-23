from rest_framework import serializers
from .models import Category

"""
class CategorySerializer(serializers.Serializer):
    # read_only=True을 써 놓으면 내보내기만 가능하고, 받기는 제외할 수 있다.
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=50)
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices)
    # read_only=True을 써 놓으면 내보내기만 가능하고, 받기는 제외할 수 있다.
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # return Category.objects.create(name=validated_data["name"],kind=validated_data["kind"])

        # 아래는 위의 코드를 간략화한 것이다.
        # **validated_data는 validated_data의 모든 데이터를 가져온다.
        # **는 딕셔너리를 가져올 때 쓰인다.
        # {"name": "Category from DRF","kind": "rooms"}를 **를 통해 가져오면
        # name="Category from DRF",kind="rooms"로 가져온다.
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance는 현재 수정하고자 하는 카테고리이다.
        # validated_data는 수정할 데이터이다.

        # 기존의 카테고리 name인 instance.name에 data의 name을 넣는데, 만약 data에 name이 없으면 기존에 가지고 있던 instance.name을 넣는다.
        instance.name = validated_data.get("name", instance.name)
        # 기존의 카테고리 kind인 instance.kind에 data의 kind을 넣는데, 만약 data에 kind이 없으면 기존에 가지고 있던 instance.kind을 넣는다.
        instance.kind = validated_data.get("kind", instance.kind)
        # 기존의 단일 object인 instance를 저장한다.
        instance.save()
        return instance
"""


class CategorySerializer(serializers.ModelSerializer):
    # 아래의 Meta class가 위에 있는 serializer를 사용한 클래스에서 필드를 정의한 역할을 똑같이 해준다.
    # name, pk, kind, created_at를 대신 정의해주는 것이다.
    # 다만 무엇을 보여줄지 안보여줄지를 정의하는 것은 직접 써야한다.
    # 보여주는 필드를 정의할 때에는 fields라는 튜플 변수에 필드명을 넣어주면 된다. ex) fields = ("name", "pk", "kind", "created_at")
    # 만약 모든 필드를 보여주고 싶다면 fields = "__all__"을 쓰면 된다.
    # 보여주지 않을 필드를 정의할 때에는 exclude라는 튜플 변수에 필드명을 넣어주면 된다. ex) exclude = ("name", "pk", "kind", "created_at")
    # 만약 모든 필드를 보여주고 싶지 않다면 exclude = "__all__"을 쓰면 된다.
    # fields와 exclude를 같이 쓸 수 없다.
    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )

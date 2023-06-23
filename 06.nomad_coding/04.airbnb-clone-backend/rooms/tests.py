from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity description test"
    URL = "/api/v1/rooms/amenities/"

    # setUp()은 테스트를 실행하기 전에 실행되는 함수이다. __init__과 같다고 볼 수 있다.
    # setUp()에서는 테스트에 필요한 데이터를 생성한다.
    # setUp()에서 생성한 데이터는 테스트가 끝나면 자동으로 삭제된다.
    # setUp()에서 생성한 데이터는 테스트 메소드에서 self.변수명으로 사용할 수 있다.
    # 다시말해 setUp은 test환경을 성정하는 메소드이다.
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,  # 1번째 인자는 변수명을 넣어준다.
            200,  # 2번째 인자는 변수에서 우리가 원하는 값을 넣어준다.
            "Status code isn't 200",  # 3번째 인자는 에러가 발생했을 때 출력할 메시지를 넣어준다.
        )
        self.assertIsInstance(  # data가 list인지 확인한다.
            data,
            list,
        )
        self.assertEqual(  # data의 길이가 1인지 확인한다.
            len(data),
            1,
        )
        self.assertEqual(  # data의 첫번째 요소의 name이 self.NAME과 같은지 확인한다.
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(  # data의 첫번째 요소의 description이 self.DESC와 같은지 확인한다.
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."

        response = self.client.post(  # URL에 json형식으로 데이터를 보낸다.
            self.URL,
            data={"name": new_amenity_name, "description": new_amenity_description},
        )
        data = response.json()

        self.assertEqual(  # 응답코드가 200인지 확인
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(  # data의 name이 우리가 보낸 값과 같은지 확인
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(  # data의 description이 우리가 보낸 값과 같은지 확인
            data["description"],
            new_amenity_description,
        )

        response = self.client.post(self.URL)  # 오류가 발생하는지 확인하는 테스트
        self.assertEqual(
            response.status_code,
            400,
            "Not 400 status code",
        )
        self.assertIn("name", data)  # data에 name이라는 키가 있는지 확인


class TestAmenity(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Dsc."
    URL = "/api/v1/rooms/amenities/1/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2/")
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        data = response.json()
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        response = self.client.put("/api/v1/rooms/amenities/2/")
        self.assertEqual(
            response.status_code,
            404,
            "Not 404 status code",
        )

        response = self.client.put(
            self.URL,
            data={
                "name": "sdfgsdfghsdfhgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgsdfgdfgssdfgsdfgsdfgsdfgsdfgsdfgsdfg"
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "Not 400 status code",
        )

        response = self.client.put(self.URL, data={"name": "New Name"})
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            "New Name",
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

        response = self.client.put(self.URL, data={"description": "New Desc."})
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["description"],
            "New Desc.",
        )
        self.assertEqual(
            data["name"],
            "New Name",
        )

    def test_delete_amenity(self):
        response = self.client.delete(self.URL)
        self.assertEqual(
            response.status_code,
            204,
            "Not 204 status code",
        )


class TestRooms(APITestCase):

    def setUp(self):
        # 유저 생성
        user = User.objects.create(
            username="test",
        )
        user.set_password("1234")  # 비밀번호 설정
        user.save()  # 저장
        self.user = user


    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(
            response.status_code,
            403,
            "Not 403 status code",
        )
        print(response.json())


        # self.client.login(  # 로그인방법 1
        #     username="test",
        #     password="1234",
        # )

        self.client.force_login(self.user)  # 로그인방법 2

        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(
            response.status_code,
            400,
            "Not 400 status code",
        )
        print(response.json())

        response = self.client.post(
            "/api/v1/rooms/",
            data={
                "price": "",
                "rooms": "",
                "toilets": "",
                "description": "",
                "address": "",
                "kind": ""
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "Not 400 status code",
        )


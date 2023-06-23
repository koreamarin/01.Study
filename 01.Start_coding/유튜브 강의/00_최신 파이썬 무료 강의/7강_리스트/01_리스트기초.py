# name = ["이영희","류지원","류화정"]    --> 이 배열을 파이썬에서는 리스트라 하고, 각 번호들을 인덱스라고 한다. ex) name[0]은 name 리스트의 0번 인덱스.


# 리스트 생성하기
animals = ["사자", "호랑이", "고양이", "강아지"]
print("리스트 생성하기")
print(animals)
print("\n")

# 리스트[인덱스]를 이용하여 데이터 접근하기.
print("리스트[인덱스]를 이용하여 데이터 접근하기")
name = animals[0]

print(name)         #사자
print(animals[1])   #호랑이
print(animals[2])   #고양이
print(animals[3])   #강아지
print("\n")

# 리스트에 데이터 추가하기. --> 리스트.append(데이터) : 이 것을 사용하면 리스트의 가장 마지막 인덱스에 데이터가 추가된다.
print("리스트에 데이터 추가하기")
animals.append("쥐")
animals.append(1000)            #--> 꼭 같은 자료형이 아니여도 된다.
print(animals)
print(animals[4])
print(animals[5])
print("\n")

# 리스트에서 데이터 삭제하기. --> del 리스트[인덱스] : 이 것을 사용하면 리스트에서 인덱스번호에 해당하는 데이터가 삭제된다. 그리고 인덱스배열이 순서에 맞게 다시 배치된다.
print("리스트에서 데이터 삭제하기")
del animals[2]      # 고양이 데이터 삭제. 2번째 인덱스가 삭제되었으므로 3번째 인덱스가 2번째 인덱스로 자동으로 앞당겨와진다.
del animals[-1]     # 마지막 데이터 삭제라는 뜻.   [-2]를 쓰면 마지막에서 두번째 데이터가 삭제된다. (-) 부호를 사용하여 뒤에서부터 인덱스 불러오기가 가능하다.

print(animals)      # 고양이, 1000이 삭제되어 사자, 호랑이, 강아지, 쥐 출력
print("\n")

# 리스트 슬라이싱 --> 리스트[시작인덱스:끝인덱스+1] : 리스트를 잘라서 다른 곳에 붙일 수 있다. ctrl + c, ctrl + v라고 생각하면 된다. 리스트 슬라이싱을 사용하였다고 해서 기존 리스트에 데이터가 사라지지 않는다. 잘라냈다는 개념과 혼동하지 말기. 복붙이라고 생각하기.
print("리스트 슬라이싱")
slicing = animals[1:3]      # animals의 1번, 2번 인덱스를 잘라서 slicing에 넣는다.
#print(slicing)
#print(animals)
print("slicing 리스트 : " + slicing[0] + ", " + slicing[-1])   # 리스트의 각 인덱스들은 지정한 자료형이 부여된다., -1인덱스는 뒤에서 첫번째 인덱스를 뜻한다.
print("animals 리스트 : " + str(animals))               # 리스트 자체는 문자형, 정수형 등 자료형이 부여되지 않는듯 하다. 리스트형 자체로 부여되는 것 같아 오류가 출력되는데, 문자형 변환을 해주면 리스트가 문자형으로 형변환 하여 출력이 가능하다.
print("\n")

# 리스트 길이 --> len(리스트) : 리스트의 개수를 정수로 나타내어주는 명령어.
print("리스트 길이 나타내어주기.")
length = len(animals)
print(length)

print(len(animals))

# 리스트 정렬
# 리스트.sort() : 알파벳, 숫자, 한글 등의 문자를 오름순서대로 맞춰주는 정렬 명령어.
# 리스트.sort(reverse=True) : 내림차순으로 정렬.
animals.sort() #오름차순 정렬
print(animals)

animals.sort(reverse=True)
print(animals)
# 반복문에서는 range(숫자)라는 함수가 많이 사용된다.
# range(10)을 쓰면 0~9까지 순서열을 반환시켜 주는데, 이 순서열을 이용하면 반복문을 쉽게 사용할 수 있다.

for i in range(10) :                # range(min, max, step)
    print(i+1, "분")

# range(1,10)을 쓰면 1~9까지 순서열을 반환시켜 준다. 시작 숫자를 지정해 줄 수 있다는 뜻이다.
for i in range(1,10) :
    print(i+1, "분")
# 함수정의방법
# def 함수이름(매개변수) : 
#   명령블록
#   return 리턴값

import random       # random 함수를 사용하기 위한 라이브러리



#매개변수와 리턴값이 둘 다 있는 형태.
def sum(a,b) :
    result = a + b
    return result


# 함수에 꼭 매개변수가 있어야 할 필요는 없다.
def getRandomNumber() : 
    number = random.randint(1,10)
    return number

# 리턴값이 꼭 없어도 된다.
def printName(name) :
    print(name)

# 매개변수와 리턴값이 둘 다 없어도 된다.
def sayHI():
    print("안녕")


x = sum(1,2)
print(x)
y = sum(5,6)
print(y)

print(getRandomNumber())

printName("안녕하세용")

sayHI()

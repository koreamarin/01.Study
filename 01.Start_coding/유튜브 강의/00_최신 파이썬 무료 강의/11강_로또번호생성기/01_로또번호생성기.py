# 로또 번호 6개 생성
# 로또 번호는 1~45까지의 랜덤한 번호
# 6개의 숫자 모두 다른 숫자.
# 로또 번호 생성함수를 작성하고 사용한다.

import random

Lotto_number = []                               #로또 번호를 저장할 리스트 생성


def LottoMaker () :                             #로또 번호 생성 함수 1~45 사이의 랜덤 숫자 생성
    number = random.randint(1,45)
    return number


while True :                                    #
    Random_num = LottoMaker()

    if Random_num not in Lotto_number : 
        Lotto_number.append(Random_num)
    
    if len(Lotto_number) == 6 :
        break

print(Lotto_number)
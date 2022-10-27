#현재 주가에 따라 매수, 매도, 대기를 하는 프로그램.


samsung = int(input("삼성전자의 현재 주가를 입력하세요. >>> "))

if samsung >= 90000 :
    print("매도합니다.")

elif samsung >= 80000 :
    print("대기중입니다.")

else :
    print("매수합니다.")


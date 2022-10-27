#가방, 시계의 합계 금액에 따라 할인률을 정해주고 할인적용 금액을 출력하는 프로그램.

bag_price = int(input("가방의 가격을 입력해주세요. >>> "))
watch_price = int(input("시계의 가격을 입력해주세요. >>> "))

total_price = bag_price + watch_price

print("합계금액은 " + str(total_price) + "입니다.")

if total_price >= 100000 :
    print("할인률은 30% 입니다.")
    total_price = total_price * 0.7

elif total_price >= 50000 :
    print("할인률은 20% 입니다.")
    total_price = total_price * 0.8

else :
    print("할인률은 10% 입니다.")
    total_price = total_price * 0.9

print("할인 적용 가격은 " + str(total_price) + "입니다.")
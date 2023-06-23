import datetime as dt

# now 클래스 설명
now = dt.datetime.now()
print(f'날짜 및 시간 : {now}')
print(f'{now.year}y')
print(f'{now.month}m')
print(f'{now.day}d')
print(f'{now.hour}h')
print(f'{now.minute}m')
print(f'{now.second}s')
print(f'{now.microsecond}us')

if now.weekday() == 0 :
    print('월요일')
elif now.weekday() == 1 :
    print('화요일')
elif now.weekday() == 2 :
    print('수요일')
elif now.weekday() == 3 :
    print('목요일')
elif now.weekday() == 4 :
    print('금요일')
elif now.weekday() == 5 :
    print('토요일')
elif now.weekday() == 6 :
    print('일요일')

print()

# today 클래스 설명
today = dt.datetime.today()
print(f'날짜 및 시간 : {today}')
print(f'{today.year}y')
print(f'{today.month}m')
print(f'{today.day}d')
print(f'{today.hour}h')
print(f'{today.minute}m')
print(f'{today.second}s')
print(f'{today.microsecond}us')

print(today.strftime('%Y년 %m월 %d일 %H시 %M분 %S초'))
print(today.strftime('영어 월 %B'))
print(today.strftime('영어 요일 %A'))
print()



# ------------------------------------------------
# timedelta 클래스 설명. 
# timedelta의 단점은 일수단위, 초단위로 차를 계산할 수 있다는 것이다. 월단위, 시간단위 등의 계산방식이 없다는 것이 단점.
dt1 = dt.datetime(2022,7,30,12,50,22,50)
dt2 = dt.datetime(2022,6,16,6,10,30,10)
td = dt1 - dt2

print(td)
print(td.days)              # dt1과 dt2의 일수 차를 나타낸 속성.
print(td.seconds)           # dt1과 dt2의 일수를 제외한 시간차를 sec로 나타낸 속성
print(td.microseconds)      # dt1과 dt2의 us차를 나타낸 속성

print(td.total_seconds())   # dt1과 dt2의 일수를 포함한 모든 시간차를 sec로 나타낸 매서드


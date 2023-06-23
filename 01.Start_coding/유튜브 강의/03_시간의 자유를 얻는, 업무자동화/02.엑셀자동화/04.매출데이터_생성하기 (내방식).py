import openpyxl
import random

# 새로운 엑셀 파일 생성
wb = openpyxl.Workbook()

# 현재 활성화된 시트 선택
ws = wb.active

# 시트 이름 변경
ws.title = "data"

# 헤더 추가
ws.append(['순번','제품명', '가격', '수량', '합계'])

# 데이터 추가
name_list = ['기계식 키보드', '게이밍 마우스', '32인치 모니터', '마우스 패드']
price_list = [120000,40000,350000,20000]

for i in range(random.randint(5,10)):
    j = random.randint(0,3)
    amount = int(random.gauss(0,2))
    if amount < 0 :
        amount = amount * -1
    amount = amount + 1

    ws.append([i+1,name_list[j],price_list[j],amount,f'=C{i+2}*D{i+2}'])
    print(i+1,name_list[j],price_list[j],amount,price_list[j]*amount)

# 저장
wb.save("startcoding\유튜브 강의\03_시간의 자유를 얻는, 업무자동화\02.엑셀자동화\11번가(내방식).xlsx")








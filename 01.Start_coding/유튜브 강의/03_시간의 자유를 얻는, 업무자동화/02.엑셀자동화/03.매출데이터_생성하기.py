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

for i in range(random.randint(5,10)) : 
    name = random.choice(name_list)         # 리스트 중에서 하나의 인덱스를 선택하는 랜덤함수.
    if name == "기계식 키보드":
        price = 120000
    elif name == "게이밍 마우스":
        price = 40000
    elif name == "32인치 모니터":
        price = 350000
    elif name == "마우스 패드":
        price = 20000
    ws.append([i+1,name,price,random.randint(1,5),f'=C{i+2}*D{i+2}'])

# 저장
wb.save(r"startcoding\유튜브 강의\03_시간의 자유를 얻는, 업무자동화\02.엑셀자동화\11번가.xlsx")




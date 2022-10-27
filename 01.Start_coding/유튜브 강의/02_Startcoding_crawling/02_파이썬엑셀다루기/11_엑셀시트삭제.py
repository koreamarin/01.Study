import openpyxl

# 1) 엑셀 불러오기
wb = openpyxl.load_workbook(r'C:\Users\USER\OneDrive\바탕 화면\startcoding\Startcoding_crawling\02_파이썬엑셀다루기\참가자_data.xlsx')

# 2) 엑셀 시트선택

ws = wb['오징어게임']

# 시트를 삭제하는 함수.
wb.remove_sheet(wb['Sheet'])

wb.save(r'C:\Users\USER\OneDrive\바탕 화면\startcoding\Startcoding_crawling\02_파이썬엑셀다루기\참가자_data.xlsx')




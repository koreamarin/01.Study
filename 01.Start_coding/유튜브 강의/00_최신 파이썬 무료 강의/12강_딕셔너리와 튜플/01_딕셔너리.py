# 1. 승패여부
# 2. 챔피언 이름
# 3. 킬
# 4. 데스
# 5. 어시스트

# 변수를 사용할 때              --> 변수가 너무 많아 관리가 어렵다.
result1 = '승리'
champ_name1 = '비에고'
kill1 = 13
death1 = 9
assist1 = 17

result2 = '패배'
champ_name2 = '베인'
kill2 = 0
death2 = 12
assist2 = 3

# 리스트를 사용할 때            --> 리스트의 각 인덱션이 무엇을 의미하는지 파악하기 어렵다.
list_play_data1 = ['승리', '비에고', 13, 9, 17]
list_play_data2 = ['패배', '베인', 0, 12, 3]


# 딕셔너리를 사용할 때          --> 키와 값의 쌍으로 이루어진 자료형, 각 데이터가 무엇을 의미하는지 알아보기 쉽다.

    # 딕셔너리 생성 방법 --> 딕셔너리이름 = {키1: 값1, 키2 : 값2, 키3 : 값3, 키4 : 값4}
dic_play_data1 = {
    'result' : '승리',
    'champ_name' : '비에고',
    'kill' : 13,
    'death' : 9,
    'assist' : 13
}

dic_play_data2 = {
    'result' : '패배',
    'champ_name' : '베인',
    'kill' : 0,
    'death' : 12,
    'assist' : 3
}

# 딕셔너리 접근 방법
    # 딕셔너리 모든 키 + 값 불러오기 : 딕셔너리이름
    # 딕셔너리 값 불러오기 : 딕셔너리이름['키 이름']
print(dic_play_data1)               # 딕셔너리의 키와 데이터 모두 접근
print(dic_play_data1['result'])     # 딕셔너리의 result키의 데이터만 접근
print(dic_play_data1['champ_name']) # 딕셔너리의 champ_name키의 데이터만 접근
print(dic_play_data1['kill'])       # 딕셔너리의 kill키의 데이터만 접근
print(dic_play_data1['death'])      # 딕셔너리의 death키의 데이터만 접근
print(dic_play_data1['assist'])     # 딕셔너리의 assist키의 데이터만 접근

print("\n")

print(dic_play_data2)
print(dic_play_data2['result'])
print(dic_play_data2['champ_name'])
print(dic_play_data2['kill'])
print(dic_play_data2['death'])
print(dic_play_data2['assist'])

print("\n")

    # 딕셔너리 값 수정/변경
dic_play_data1['result'] = '패배'           # 기존 값 변경
        
dic_play_data1['level'] = 18                # 새로운 키, 값 추가
        
del dic_play_data1['champ_name']            # 데이터 삭제

print(dic_play_data1)
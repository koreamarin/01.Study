# 딕셔너리 관련함수     모든 딕셔너리 관련함수는 for in 문과 함께 자주쓰인다.
# keys()
# values()
# items()

play_data1 = {
    'result' : '승리',
    'champ_name' : '비에고',
    'kill' : 13,
    'death' : 9,
    'assist' : 13
}

# keys()
for key in play_data1.keys() :          # key에 해당하는 key name을 출력
    print(key)

print('\n')

# values ()                             # 값에 해당하는 value 값 출력.
for value in play_data1.values():
    print(value)

print('\n')

# item ()
for key, value in play_data1.items() :
    print(key, value)

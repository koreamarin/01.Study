# cmd 창에 pip install pyautogui 입력하여 라이브러리 설치
import pyautogui
import time



# 1. 화면 크기 출력
print(pyautogui.size())

# 2. 마우스 위치 출력
# i=0
# while True :
#     time.sleep(0.1)
#     print(pyautogui.position())     # 마우스 위치 출력 함수.
#     i = i+1

# 3. 마우스 이동 (듀얼모니터 가능)
# pyautogui.moveTo(-1972,370)             #(x축, y축)
# pyautogui.moveTo(1972,900,3)            #(x축, y축, 이동딜레이)

# 4. 마우스 클릭
# pyautogui.click()                           # 왼쪽 클릭
# pyautogui.click(button='right')             # 오른쪽 클릭
# pyautogui.doubleClick()                     # 더블 클릭
# pyautogui.click(clicks=3, interval=1)       # 3번 클릭할건데 1초마다 클릭

# 5. 마우스 드래그
# 416,46 -> 737,57
pyautogui.moveTo(416,43)
pyautogui.dragTo(737,43,0.5)
# 578,43 -> 379,79
pyautogui.moveTo(578,43)
pyautogui.dragTo(350,43,0.5)





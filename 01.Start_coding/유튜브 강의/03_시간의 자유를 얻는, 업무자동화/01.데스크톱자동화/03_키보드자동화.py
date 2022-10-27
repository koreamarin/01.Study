import pyautogui
import pyperclip

# 1. 키보드 입력 (문자)
# pyautogui.write('startcoding', interval=0.25)
# pyautogui.write('한글지원안해요...')

# 2. 키보드 입력 (키)
# pyautogui.press('enter')
# pyautogui.press('up')

# 3. 키보드 입력 (여러개 동시 키입력)
# pyautogui.hotkey('ctrl', 'c')

# 4. 한글입력방법
pyperclip.copy('한글쓰고싶으면 이 방법 써야함')         # 클립보드안에 텍스트 복사
pyautogui.hotkey('ctrl', 'v')


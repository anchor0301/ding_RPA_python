import pyautogui as py

# 마우스 이동
py.moveTo(100, 100)  # 지정한 위치로 이동(절대값)

py.moveTo(200, 200, duration=0.25)

py.moveTo(300, 200, duration=0.25)
py.moveTo(100,100 ,duration=0.5)
print("프로그램 종료")
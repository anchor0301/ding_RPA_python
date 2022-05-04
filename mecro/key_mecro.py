import pyautogui as pag
import keyboard
import time
while True:
    if keyboard.is_pressed("F4"): # F4 누른게 감지되면
        t1 = pag.position() # 위치 뽑아서 저장
        print(t1)
        time.sleep(0.5)
        break        
while True:
    if keyboard.is_pressed("F4"): 
        t2 = pag.position()
        print(t2)
        time.sleep(0.5)
        break
import re

import keyboard as keyboard
import pyautogui
import time
import os
import threading
def enter():
    while True:
        pyautogui.press('enter')
        print("정지 'F4' 입력")

        if keyboard.is_pressed('F4'):
            print("정지")
            break

print("엔터 입력 프로그램 시작")
print("시작 'F2' 입력")
while True:
    if keyboard.is_pressed('F2'):
        print("정지하려면 'F4' 입력")
        enter()
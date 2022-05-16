import threading
from time import sleep
import find_register
import main
def hello_1():
    main.main()

def find_register():
    find_register.main()

def hello_1_thread():
    thread=threading.Thread(target=hello_1) #thread를 동작시킬 함수를 target 에 대입해줍니다
    thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
    thread.start() #thread를 시작합니다

if __name__ == "__main__":
    hello_1_thread()
    find_register()

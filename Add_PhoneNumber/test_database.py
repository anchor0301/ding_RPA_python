import threading
import time

from def_notion import rest_exit_database


def printhelloWorld():
    print("HelloWorld")

    # 5초마다 printhelloWorld함수를 반복 수행

    threading.Timer(1, printhelloWorld).start()

def printhelloWorld1():
    print("HelloWorld111")

    # 5초마다 printhelloWorld함수를 반복 수행

    threading.Timer(1, printhelloWorld1).start()

def notion():
    rest_exit_database()

    # 5초마다 printhelloWorld함수를 반복 수행

    threading.Timer(1250, notion).start()


def main():
    print("에러 발생")
    return 0 / 0




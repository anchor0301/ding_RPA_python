# ftp_server.py
import os

import datetime
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# ftp_server_auth.py
FTP_HOST = '172.30.1.47'  # TODO 아이피 수정
FTP_PORT = 9021

now = datetime.datetime.now()

now_time = now.strftime("%y-%m-%d")

path_dir = "/Users/anchor/Desktop/사진"

file_list = os.listdir(path_dir)


def select_dir():

    print(file_list.sort(reverse=True))

    print("-------------")

    for i in range(3, 8):
        create_time = os.path.getctime(f'{path_dir}/{file_list[i]}')
        create_time = datetime.datetime.fromtimestamp(create_time)
        create_time = datetime.datetime.strftime(create_time, '%Y-%m-%d %H:%M')

        print(f'[{i - 2}]', end="\t  ")
        print(file_list[i], end="\t")
        print(create_time)

    num = int(input("저장할 폴더의 숫자를 입력하세요 / 새 폴더 만들기 : 0  > "))

    if num == 0:

        now = datetime.datetime.now()

        now_time = now.strftime("%y-%m-%d")

        name = input("폴더명을 입력해주세요 > ")
        folder_name = f'{now_time} {name}'

        print(f"[{folder_name}]폴더가 생성됨")
        os.mkdir(f"/Users/anchor/Desktop/사진/{folder_name}")

        return folder_name

    elif num <= 5:
        print("")
        folder_name = file_list[num + 2]
        print(f"[{folder_name}]폴더를 선택함")

        return folder_name


def main():
    folder_name = select_dir()
    ftp_admin_dir = os.path.join(path_dir, folder_name)

    authorizer = DummyAuthorizer()

    authorizer.add_user('admin', 'admin1234', ftp_admin_dir, perm='elradfmwMT')

    handler = FTPHandler
    handler.banner = "Welcome FTP Server."

    handler.authorizer = authorizer
    handler.passive_ports = range(9021, 65535)

    address = (FTP_HOST, FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()


if __name__ == '__main__':
    main()

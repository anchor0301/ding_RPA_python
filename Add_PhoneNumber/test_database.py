from __future__ import print_function

import os

import gspread
import httplib2
import pymysql
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

import hide_api

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = "aaaa.json"
APPLICATION_NAME = 'People API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('./')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'people.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())

###############################    gpread코드    ##############################################################

scopee = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = "ding.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scopee)
gc = gspread.authorize(credentials)

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(hide_api.spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')


# TODO 테스트용 삭제하기!
def ss(ss):
    print(worksheet.get("i1:i" + str(ss)))


db_connect = pymysql.connect(
    host="localhost",
    port=3306,
    db="user_db",
    user='root',
    passwd='0000',
    charset='utf8'
)
db_connected = db_connect.cursor()
# sql_cmd = "create database user_db;"  # 데이터베이스 생성
# sql_cmd = "delete database user_profile;"  # 데이터베이스 삭제

create_table = "create table dog_info (" \
               "BOOK_ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT," \
               "SERVICE VARCHAR(10) NOT NULL," \
               "CHECK_IN DATETIME," \
               "CHECK_OUT DATETIME," \
               "TIMESTAMP DATETIME," \
               "CUST_NUMBER INT(11) UNSIGNED NOT NULL ," \
               "PRIMARY KEY(BOOK_ID))"


insert_table = "insert into user_profile " \
               "(OWNER_NAME,PHONE_NUMBER)" \
               "values" \
               "(%s, %s)"

delete_table = "delete from user_profile where *"

# 증가 초기화 명령어
init_table = "ALTER TABLE user_profile AUTO_INCREMENT = 1;"

print(db_connected.execute(create_table))
# print(db_connected.execute(insert_table, ("김지호", "01045900004")))

# print(db_connected.execute(insert_table, ("김성민", "01089000137")))

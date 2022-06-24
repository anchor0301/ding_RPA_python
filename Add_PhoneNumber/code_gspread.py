from __future__ import print_function
import time
import re
import gspread
import httplib2
import datetime
from dateutil.parser import parse
from datetime import datetime
from datetime import timedelta
import os
import hide_api
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
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


# 현재 스프레드시트의 의 갯수를 출력한다.
def last_col_info(add_number):
    list_of_dicts = worksheet.row_values(add_number)
    data_list = {
        # 딕셔너리 형태로
        # 요소들을 하나씩 넣음

        'service': list_of_dicts[3],  # 서비스
        'host_name': list_of_dicts[4],  # 견주이름
        'phoneNumber': list_of_dicts[5],  # 전화번호

        'start_day': list_of_dicts[6],  # 입실일
        'end_day': list_of_dicts[7],  # 퇴실일

        'dog_name': list_of_dicts[8],  # 애견이름
        'sex': list_of_dicts[9],  # 성별
        'weight': list_of_dicts[10],  # 몸무게
        'breed': list_of_dicts[11],  # 견종
        'others': list_of_dicts[15],  # 특이사항
        "useTime": "0"  # 카운트
    }
    if data_list.get("end_day"):
        pass
    else:

        data_list["start_day"] = str(datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
        data_list["end_day"] = str((datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y %H:%M:%S'))
        data_list["useTime"]=list_of_dicts[17]  # 카운트

    return data_list


#  i 애견이름/l 견종/d 서비스/f 전화번호


def creat_a_google_contact(dog):  # 구글 주소록에 연락처를 추가하는 api 입니다.

    print(dog.phoneNumber, "번 행의 연락처를 등록합니다.")

    service = discovery.build('people', 'v1', http=http,
                              discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
    service.people().createContact(body={
        "names": [
            {
                'givenName': f"{dog.Info()}"
            }
        ],
        "phoneNumbers": [
            {
                'value': f"{dog.phoneNumber}"
            }
        ]
    }).execute()

    print("등록 완료")


# 테스트 용
#last_col_info(332)
#print(creat_a_google_contact(17))

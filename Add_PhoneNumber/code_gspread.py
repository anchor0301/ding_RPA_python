from __future__ import print_function
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials


import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = 'aaaa.json'
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
json_file_name = 'ding.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scopee)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/12BZajvryk9dE6cVQ0wwbXaKvK22xLCXFeEWTptfXkfY/edit?usp=sharing'
# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')


# 현재 스프레드시트의 행의 갯수를 출력한다.
def last_col_info(row_number,i):
    return worksheet.acell(row_number + str(i)).value


#  i 애견이름/l 견종/d 서비스/f 전화번호
def last_info(i):
    dog_name = last_col_info("i",i)  # i 애견이름
    dog_breed = last_col_info("l",i)  # l 견종
    service = last_col_info("d",i)  # d 서비스
    phone_numbers = last_col_info("f",i)  # f 전화번호

    # 견종 중 괄호안의 글자 삭제
    rm_breed = re.sub(r'\([^)]*\)', '', dog_breed)

    # 연락처 이름을 저장한다
    # ex) 뚱/포메/호/1234
    print_last_info = f"{dog_name}/{rm_breed.rstrip()}/{service[0]}/{phone_numbers[7:]}"

    return print_last_info



def creat_a_google_contact(i): #구글 주소록에 연락처를 추가하는 api 입니다.
    print(i,"번 행의 연락처가 등록됨")
    pass
    service = discovery.build('people', 'v1', http=http,
                              discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
    service.people().createContact(body={
        "names": [
            {
                'givenName': f"{last_info()}"
            }
        ],
        "phoneNumbers": [
            {
                'value': f"{last_col_info('f',i)}"
            }
        ]
    }).execute()

    print("등록 완료")

creat_a_google_contact()




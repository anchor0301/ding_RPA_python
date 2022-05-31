from Add_PhoneNumber.code_gspread import *
import time

from dateutil.parser import parse

start = time.time()  # 시작 시간 저장


list_of_dicts = worksheet.get_all_records()

for dic in list_of_dicts[2:3]:  # 튜플 안의 데이터를 하나씩 조회해서
    data_list = []
    print(dic)
    data_dic = {  # 딕셔너리 형태로
        # 요소들을 하나씩 넣음
        'host_name':list(dic.values())[4],
        'dog_name': list(dic.values())[8],
        'breed': list(dic.values())[9],
        'PhoneNumber': "0" + str(list(dic.values())[5])
    }
    data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음


for obj in data_list:
    print(obj.get("dog_name"))
    print(obj.get("breed"))
    print(obj.get("PhoneNumber"))
    print("____________")
new_inform=last_col_info(4)
print(new_inform.get("host_name"))

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
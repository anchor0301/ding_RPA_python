from Add_PhoneNumber.code_gspread import *

last_n = worksheet.col_values(6)
last_a = len(last_n)

list_of_dicts = worksheet.get_all_records()
data_list = []
i = 4
for dic in list_of_dicts[-5:]:  # 튜플 안의 데이터를 하나씩 조회해서

    data_dic = {  # 딕셔너리 형태로
        # 요소들을 하나씩 넣음

        'cust_number': last_a - i,
        'dog_name': list(dic.values())[8],
        'breed': list(dic.values())[9],
        'PhoneNumber': "0" + str(list(dic.values())[5])
    }
    i = i - 1
    data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음
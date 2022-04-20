last_a = 17
new_a =19

def last_col_info(row_number,i):
    return print(f"워크시트{new_a - i}번째 투플을 추가함 ")

for i in reversed(range(0,new_a - last_a)):


    last_col_info("i",i)

    last_a = new_a
print("------------------------")
print("마지막으로 저장된 행 번호 : ",last_a)



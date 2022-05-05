last_a = 23
new_a =25

def last_col_info(row_number,i):
    return print(f"워크시트{new_a - i}번째 투플을 추가함 ")

for i in reversed(range(0,new_a - last_a)):

    print("현재 실행중인 행 번호 : " ,(new_a-i))
    last_col_info("i",(new_a-i))


last_a = new_a
print("________________\n")
print("마지막으로 저장된 행 번호 : ",last_a)



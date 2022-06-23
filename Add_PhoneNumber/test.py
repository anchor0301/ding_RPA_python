
from puppyInfo import puppyInformation
from code_gspread import last_col_info
dog = puppyInformation(last_col_info(17))

print(dog.dog_name)

def 아무거나(ddd):
    print(ddd)

아무거나(dog.dog_name)
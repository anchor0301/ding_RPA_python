from line_notify import LineNotify

new_name="성민"
new_n="01089000137"
start_day="02-Feb-2022 02:03:00"
end_day="04-Feb-2022 02:02:00"
ACCESS_TOKEN = "dWjAqgCfy7xE7lDyj2EYL3v1VZ1tr2z0miLWlle7s4r"
notify = LineNotify(ACCESS_TOKEN)
notify.send(f"새로운 연락처가 추가되었습니다. \n"
                        f"\n이름 : {new_name} "
                        f"\n연락처 : {new_n}"
                        f"\n시작일 :  {start_day}"
                        f"\n종료일 : {end_day}")
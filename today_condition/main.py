from PIL import Image, ImageDraw, ImageFont
import datetime

im = Image.open("img/condition_card.png")
draw = ImageDraw.Draw(im)


def init():
    global dog_name
    global service_type
    global lunch_eat
    global dinner_eat
    global lunch_Snack_eat
    global dinner_Snack_eat
    global condition

    dog_name = "가을이"  # 삭제삭제삭제삭제삭제삭제삭제삭제
    service_type = "1"  # 삭제삭제삭제삭제삭제삭제삭제삭제
    lunch_eat = "2"
    dinner_eat = "1"

    lunch_Snack_eat = "4"
    dinner_Snack_eat = "3"

    condition = "5"


def create_condition():
    global dog_name
    dog_name = input("강아지 이름 : ")
    draw.text((280, 190), f"{dog_name}의 하루", font=ImageFont.truetype("img/Maplestory Bold.ttf", 50), fill=(0, 0, 0))
    im.save(f"card/{dog_name}_card.png")


def use_service_date():
    d = datetime.datetime.now()
    draw.text((533, 285), f"{d.month}", font=ImageFont.truetype("img/Maplestory Bold.ttf", 30), fill=(0, 0, 0))
    draw.text((617, 285), f"{d.day}", font=ImageFont.truetype("img/Maplestory Bold.ttf", 30), fill=(0, 0, 0))


def check(x, y):
    my_image = Image.open(f'card/{dog_name}_card.png')
    watermark = Image.open('img/check.png')
    watermark = watermark.resize((60, 60))  # 230px 60px 로 워터마크 사진 크기 조절

    my_image.paste(watermark, (x, y), watermark)
    my_image.save(f"card/{dog_name}_card.png")


def service_state_check():
    service_type = input("이용한 서비스는 무엇인가요? \n 1. 호텔링   2. 놀이방 : ")

    if service_type == "1":
        check(70, 260)  # 호텔
    else:
        check(193, 260)  # 놀이방


def fead_state_cheak():
    lunch_eat = input("점심밥을 다 먹었나요? \n 1. 남음   2. 다 먹음 : ")
    dinner_eat = input("저녁밥을 다 먹었나요? \n 1. 남음   2. 다 먹음 : ")

    # 점심
    if lunch_eat == "1":
        check(148, 379)  # 남음
    else:
        check(271, 379)  # 다 먹음
    # 저녁
    if dinner_eat == "1":
        check(148, 435)  # 남음
    else:
        check(271, 435)  # 다 먹음


def Snack_cheak():
    lunch_Snack_eat = input("점심 간식을 다 먹었나요? \n 1. 남음   2. 다 먹음 : ")
    dinner_Snack_eat = input("저녁 간식을 다 먹었나요? \n 1. 남음   2. 다 먹음 : ")

    # 점심
    if lunch_Snack_eat == "1":
        check(148, 545)  # 남음
    else:
        check(271, 545)  # 다 먹음
    # 저녁
    if dinner_Snack_eat == "1":
        check(148, 600)  # 남음
    else:
        check(271, 600)  # 다 먹음


def feces_state():
    lunch_Snack_eat = input("점심 배변상태는 어떤가요? \n 1. 정상   2. 살짝 묽음 3. 묽음   4. 나쁨 : ")
    dinner_Snack_eat = input("저녁 배변상태는 어떤가요? \n 1. 정상   2. 살짝 묽음 3. 묽음   4. 나쁨 : ")

    # 점심
    if lunch_Snack_eat == "2":
        check(573, 379)  # 살짝 묽음
    elif lunch_Snack_eat == "3":
        check(650, 379)  # 묽음
    elif lunch_Snack_eat == "4":
        check(711, 379)  # 나쁨
    else:
        check(495, 379)  # 정상
    # 저녁
    if dinner_Snack_eat == "2":
        check(573, 438)  # 살짝 묽음
    elif dinner_Snack_eat == "3":
        check(650, 438)  # 묽음
    elif dinner_Snack_eat == "4":
        check(711, 438)  # 나쁨
    else:
        check(495, 438)  # 정상


def doggy_condition():
    condition  = input(f"오늘 {dog_name}의 컨디션이 어떤가요? \n 1. 행복   2. 친화 3. 수면   4. 예민 : ")
    if condition == "2":
        check(455, 630)  # 예민
    elif condition == "3":
        check(575, 568)  # 친화
    elif condition == "4":
        check(660, 568)  # 수면
    else:
        check(455, 568)  # 행복


#init()  테스트용

use_service_date()  # 호텔링 이용 날짜를 기록
print("___________________________\n")
create_condition()  # 강아지 이름을 기록
print("___________________________\n")

service_state_check()  # 이용 서비스를 체크
print("___________________________\n")

fead_state_cheak()  # 식사 여부를 체크
print("___________________________\n")

Snack_cheak()  # 간식 여부 체크
print("___________________________\n")

feces_state()  # 배변 상태
print("___________________________\n")

doggy_condition()
print("___________________________\n")

print(f"{dog_name}의 관리 카드 등록 완료")
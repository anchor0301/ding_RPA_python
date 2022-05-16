def total():
    global total
    total = kor + mat + eng + sci

    return print("총점 : ", total)


def avg():
    global avg
    avg = total / 4

    return print("평균 : ", avg)


def gread():
    if avg >= 90:
        gread = "A"
    elif avg >= 80:
        gread = "B"
    elif avg >= 70:
        gread = "D"
    else:
        gread = "F"

    return  print("학점 : ", gread)


kor = int(input("국어 점수 : "))
mat = int(input("수학 점수 : "))
eng = int(input("영어 점수 : "))
sci = int(input("과학 점수 : "))

total()
avg()
gread()

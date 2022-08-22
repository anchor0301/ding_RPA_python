import re


print("Scan the barcode")
f = open("barcode.txt",'a')
while True:
    scan_in = input("Input :")
    if scan_in == 'q':   # 키보드에서 q 누르고 enter입력하면 종료
        scan_in = re.sub(r'[^0-9]', '', scan_in)
        break
    f.write("|"+scan_in+"||2")
f.close()
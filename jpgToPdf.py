# jpg to pdf with img2pdf
import os
from img2pdf import convert
from PyPDF2 import PdfMerger
import zipfile
from PIL import Image

realpath = r"/Users/anchor/Desktop/download"
absolutepath = r"images"


def jpgtopdf():
    with open("in.pdf", "wb") as f:
        image_list = []

        for file in os.listdir(realpath):
            if file.endswith(".jpg"):
                image_list.append(realpath + '/' + file)
        image_list = sorted(image_list)
        print(image_list)

        pdf = convert(image_list)
        f.write(pdf)


def ziptopdf():
    realpath = r"/Users/anchor/Desktop/"
    file_name = input("Desktop 안의 zip의 파일명 입력하세요 : ")
    # with zipfile.ZipFile(f"{realpath}{file_name}.zip", "r") as zip_ref:
    #     print(zip_ref.namelist())
    imgzip = zipfile.ZipFile(f"{realpath}{file_name}.zip", "r")
    inflist = imgzip.infolist()

    with open("in.pdf", "wb") as makepdf:

        image_list = []
        for f in inflist:
            ifile= imgzip.open(f)
            image_list.append(ifile)
        pdf = convert(image_list)
        makepdf.write(pdf)

def pdf():
    """
    pdf 합치기
    """
    pdfs = ['1.pdf', '2.pdf', "3.pdf", "4.pdf"]

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write("jung.pdf")
    merger.close()


ziptopdf()
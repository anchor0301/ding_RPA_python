
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials

import re
import gspread
import time
import chromedriver_autoinstaller

start = time.time()  ################## 기록시작
print("기록을 시작합니다.")

###############################    셀리니움 코드    ################################################

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
url = "https://contacts.google.com/new?hl=ko"
driver.get(url)
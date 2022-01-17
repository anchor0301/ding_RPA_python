from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import time
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "./chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
url="https://contacts.google.com/new?hl=ko"
driver.get(url)

#이름 추가
# 애견이름/견종/서비스/전화번호
def reg_profile(name):
    add_name=driver.find_element_by_xpath("//*[@id='c0']/div[2]/div[1]/div/div[1]/div/div[1]/input")
    add_name.send_keys(name)

#전화번호 입력
add_num=driver.find_element_by_xpath("//*[@id='c5']/div[1]/div[2]/div[1]/div/div[1]/input")
add_num.send_keys("010-1234-5678")

register=driver.find_element_by_xpath(" //*[@id='yDmH0d']/c-wiz/div/div[1]/div[1]/div/div[1]/div[2]/div[2]/button ")
register.click()

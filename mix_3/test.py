
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
url = "https://contacts.google.com/new?hl=ko"
driver.get(url)


# 이름 추가
# 애견이름/견종/서비스/전화번호
def reg_profile(name):
    add_name = driver.find_element_by_xpath("//*[@id='c0']/div[2]/div[1]/div/div[1]/div/div[1]/input")
    add_name.send_keys(name)

reg_profile("성민")
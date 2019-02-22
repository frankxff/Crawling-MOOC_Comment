from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time

url = "http://www.icourses.cn"
browser = webdriver.Chrome()
browser.get(url)
time.sleep(10)
searchBtn = browser.find_element_by_id("header-login-btn")
searchBtn.click()
#打开登录页
time.sleep(10)
browser.switch_to.frame(0)
searchName = browser.find_element_by_id("pd_web_login_name")
searchName.clear()
searchName.send_keys("username")
#输入账号

searchPwd = browser.find_element_by_id("pd_web_pwd")
searchPwd.clear()
searchPwd.send_keys("password")
#输入密码

searchBtn = browser.find_element_by_id("pd_web_btn_submit")
searchBtn.click()
#点击登录按钮
time.sleep(5)
js = " window.open('http://www.icourses.cn/web/sword/portal/shareDetails?cId=4860#/bbs/index')" #可以看到是打开新的标签页 不是窗口
browser.execute_script(js)
#打开高等数学课程评论页
time.sleep(10)

page = 0
total_list = []
while page < 266:
    browser.switch_to_window(browser.window_handles[-1])
    #定位当前页
    html = browser.page_source
    #页面代码存入html
    soup = BeautifulSoup(html ,"lxml")
    try:
        element = WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"bbs-item-title"))
        )
    finally:
        say_list = soup.find_all("a", class_="bbs-item-title")
    
    for say in say_list:
        say_item = say.get_text()
        total_list.append(say_item)
    #将当页评论放入total_list
    try:
        element = WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.XPATH,"//a[contains(text(),'下一页')]"))
        )
        element = WebDriverWait(browser,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"bbs-larPagination-box"))
        )
        element = WebDriverWait(browser,10).until(
                EC.element_to_be_clickable((By.XPATH,"//a[contains(text(),'下一页')]"))
        )
               
    finally:
        searchBtn1 = browser.find_element_by_xpath("//a[contains(text(),'下一页')]")
        searchBtn1.click()
    time.sleep(3)
    #点击下一页
math = pd.DataFrame(total_list)
writer = pd.ExcelWriter('D:/PythonOutput/MOOC高等数学评论集.xlsx')
math.to_excel(writer, '高等数学')
writer.save()
#导出为Excel文件
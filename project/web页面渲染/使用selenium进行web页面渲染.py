#coding=utf-8

"""
学习使用selenium进行web页面渲染
"""

import os

from selenium import webdriver

chromedriver = "C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"

os.environ["webdriver.chrome.driver"] = chromedriver

driver =  webdriver.Chrome(chromedriver)

driver.get("http://www.hao123.com")

driver.quit()

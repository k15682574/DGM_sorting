from selenium import webdriver
import numpy as np
import pandas as pd

stock = 'BTI'

driver = webdriver.Chrome('chromedriver')
while True:
    try:
        driver.get('https://financials.morningstar.com/ratios/r.html?t=' + stock)
        large_button = driver.find_element_by_class_name("large_button")
        large_button.click()
        break
    except:
        print("export " + stock + " failed, try again")
        continue

stock = 'AMZN'
while True:
    try:
        driver.get('https://financials.morningstar.com/ratios/r.html?t=' + stock)
        large_button = driver.find_element_by_class_name("large_button")
        large_button.click()
        break
    except:
        print("export " + stock + " failed, try again")
        continue
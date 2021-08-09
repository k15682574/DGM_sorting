from selenium import webdriver
import numpy as np
import pandas as pd
import shutil
import time

def export(category):
    df = pd.read_csv('./stock_list/' + category + '.csv', index_col='index')
    print(df.info())

    driver = webdriver.Chrome('chromedriver')
    num = 0
    trial = 0
    for stock in df['stock']:
        trial = 0
        while True:
            try:
                driver.get('https://financials.morningstar.com/ratios/r.html?t=' + stock)
                time.sleep(1)
                large_button = driver.find_element_by_class_name("large_button")
                large_button.click()
                break
            except:
                trial += 1
                if trial < 5:
                    continue
                else:
                    break

        num += 1
        if trial < 5:
            print('trial = {}, get {} {}'.format(trial, num, stock))
        else:
            print('trial = {}, fail to get {} {}'.format(trial, num, stock))

    print('finished downloading {} key ratios files.'.format(num))

    for input in df['stock']:
        stock = input.replace("/", ".")
        try:
            shutil.move('C:\\Users\\User\\Downloads\\{} Key Ratios.csv'.format(stock), 'D:\\BOS\\parsing\\key_ratios\\{}\\{} Key Ratios.csv'.format(category, stock))
        except:
            print("{} is missing".format(stock))
            continue

from selenium import webdriver
import numpy as np
import pandas as pd
import shutil

def export(category):
    df = pd.read_csv('./stock_list/' + category + '.csv', index_col='index')
    print(df.info())

    driver = webdriver.Chrome('chromedriver')
    num = 0
    for stock in df['stock']:
        while True:
            try:
                driver.get('https://financials.morningstar.com/ratios/r.html?t=' + stock)
                large_button = driver.find_element_by_class_name("large_button")
                large_button.click()
                break
            except:
                continue

        num += 1
        print('got {} {}'.format(num, stock))

    print('finished downloading {} key ratios files.'.format(num))

    for input in df['stock']:
        stock = input.replace("/", ".")
        shutil.move('C:\\Users\\User\\Downloads\\{} Key Ratios.csv'.format(stock), 'D:\\BOS\\parsing\\key_ratios\\{}\\{} Key Ratios.csv'.format(category, stock))

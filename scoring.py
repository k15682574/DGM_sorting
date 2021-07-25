import numpy as np
import pandas as pd
import csv

def find_index(datalist, key):
    for title in range(len(datalist)):
        try:
            if datalist[title][0] == key:
                return title
        except:
            continue
    
    return -1  

def scoring_E(datalist):
    eps = find_index(datalist, "Earnings Per Share USD")
    rvn = find_index(datalist, "Revenue USD Mil")
    
    if datalist[eps][10] == "":
        return "No"

    if datalist[eps][1] == "":
        return "No"

    if datalist[rvn][10] == "":
        return "No"

    if datalist[rvn][1] == "":
        return "No"

    if float(datalist[eps][10].replace(",", "")) >= float(datalist[eps][1].replace(",", "")) and float(datalist[rvn][10].replace(",", "")) >= float(datalist[rvn][1].replace(",", "")):
        return "Yes"
    else:
        return "No"

def scoring_D(datalist):
    div = find_index(datalist, "Dividends USD")
    for div_each in datalist[div][1:]:
        if div_each == "":
            return "No"

    return "Yes"

def scoring_F(datalist):
    fcf = find_index(datalist, "Free Cash Flow USD Mil")
    for fcf_each in datalist[fcf][1:]:
        if fcf_each == "":
            return "No"
        if float(fcf_each.replace(",", "")) <= 0:
            return "No"

    return "Yes"

def scoring_R(datalist):
    roe = find_index(datalist, "Return on Equity %")
    de = find_index(datalist, "Debt/Equity")
    roa = find_index(datalist, "Return on Assets %")

    roe_list = []
    for i in datalist[roe][1:11]:
        if i != "":
            roe_list.append(float(i.replace(",", "")))
        else:
            roe_list.append(0)

    roa_list = []
    for i in datalist[roa][1:11]:
        if i != "":
            roa_list.append(float(i.replace(",", "")))
        else:
            roa_list.append(0)

    if float(sum(roe_list)) / 10 > 15:
        if datalist[de][10] != "":
            if float(datalist[de][10]) < 1:
                return "Yes "

    if float(sum(roa_list)) / 10 > 7:
        return "Yes "

    return "No"
    
def scoring_I(datalist):
    ic = find_index(datalist, "Interest Coverage")

    if datalist[ic][11] == "":
        return "No Dept"

    if float(datalist[ic][11].replace(",", "")) > 10:
        return ">  10"

    if float(datalist[ic][11].replace(",", "")) > 4:
        return "> 4"

    return "No"

def scoring_N(datalist):
    nm = find_index(datalist, "Net Margin %")

    if datalist[nm][11] =="":
        return "No"

    if float(datalist[nm][11].replace(",", "")) > 20:
        return ">20%"

    if float(datalist[nm][11].replace(",", "")) > 10:
        return ">10%"
        
    for start in datalist[nm][1:11]:
        if start != "":
            if float(datalist[nm][11].replace(",", "")) > float(start.replace(",", "")):
                return "Growing"
            else:
                return "No"

    return "No"

def scoring_total(datalist):
    score = 0
    e = scoring_E(datalist)
    d = scoring_D(datalist)
    f = scoring_F(datalist)
    r = scoring_R(datalist)
    i = scoring_I(datalist)
    n = scoring_N(datalist)
    if e == "Yes":
        score += 1

    if d == "Yes":
        score += 1

    if f == "Yes":
        score += 1
    
    if r == "Yes ":
        score += 1

    if i == "No Dept" or i == ">  10":
        score += 1
    elif i == "> 4":
        score += 0.5

    if n == ">20%":
        score += 1
    elif n == ">10%" or n == "Growing":
        score += 0.5
        
    return score

def scoring(category):
    df_in = pd.read_csv('./stock_list/' + category + '.csv', index_col='index')
    print(df_in.info())

    E = []
    D = []
    F = []
    R = []
    I = []
    N = []
    score = []
    ids = []

    for input in df_in['stock']:
        stock = input.replace("/", ".")
        with open(".\\key_ratios\\{}\\{} Key Ratios.csv".format(category, stock), newline='') as csvfile:
            rows = csv.reader(csvfile)
            datalist = list(rows)

            ids.append(stock)
            E.append(scoring_E(datalist))
            F.append(scoring_F(datalist))
            R.append(scoring_R(datalist))
            I.append(scoring_I(datalist))
            N.append(scoring_N(datalist))
            D.append(scoring_D(datalist))
            score.append(scoring_total(datalist))

        df_dic = {
            'EPS': E,
            'Free Cash Flow': F,
            'ROE': R,
            'IC': I,
            "Net Margin": N,
            'Dividend': D,
            "score": score
        }
        df_out = pd.DataFrame(data=df_dic, index=ids)
        df_out.to_csv(".\\scoring\\{}.csv".format(category))

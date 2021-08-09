import numpy as np
import pandas as pd
import csv
import urllib.request as req
import bs4
import re
import pandas as pd
import numpy as np

def find_index(datalist, key):
    for title in range(len(datalist)):
        try:
            if datalist[title][0] == key:
                return title
        except:
            continue
    
    return -1  

def scoring_DG(dg5y):
    if dg5y > 10:
        return 1

    if dg5y > 6:
        return 0.5

    return 0

def scoring_F(datalist):
    fcf = find_index(datalist, "Free Cash Flow Per Share * USD")
    div = find_index(datalist, "Dividends USD")
    years = 5
    
    fcf_list = []
    for i in datalist[fcf][11-years:11]:
        if i != "":
            fcf_list.append(float(i.replace(",", "")))
        else:
            fcf_list.append(0)

    div_list = []
    for i in datalist[div][11-years:11]:
        if i != "":
            div_list.append(float(i.replace(",", "")))
        else:
            div_list.append(0)

    fcf_payout_list = []
    for i in range(len(fcf_list)):
        if fcf_list[i] != 0:
            fcf_payout_list.append(div_list[i] / fcf_list[i])
        else:
            fcf_payout_list.append(1)

    if sum(fcf_payout_list)/len(fcf_payout_list) < 0.4:
        if fcf_payout_list[len(fcf_payout_list)-1] < 0.4:
            return 1

    if sum(fcf_payout_list)/len(fcf_payout_list) < 0.75:
        if fcf_payout_list[len(fcf_payout_list)-1] < 0.75:
            return 0.5

    return 0

def scoring_RVN(datalist):
    eps = find_index(datalist, "Earnings Per Share USD")
    rvn = find_index(datalist, "Revenue USD Mil")

    if datalist[rvn][10] != "":
        rvn10 = float(datalist[rvn][10].replace(",", ""))
    else:
        rvn10 = 0
        
    if datalist[rvn][1] != "":
        rvn1 = float(datalist[rvn][1].replace(",", ""))
    else:
        rvn1 = 0
        
    if datalist[eps][10] != "":
        eps10 = float(datalist[eps][10].replace(",", ""))
    else:
        eps10 = 0
        
    if datalist[eps][1] != "":
        eps1 = float(datalist[eps][1].replace(",", ""))
    else:
        eps1 = 0
        
    if rvn10 >= rvn1*0.9:
        if eps10 >= eps1*1.2:
            return 1
        elif eps10 >= eps1*0.9:
            return 0.5

    return 0        

def scoring_EQ():
    return 1

def scoring_ER(dg5y, dg10y):
    if dg5y > dg10y:
        return 1
    else:
        return 0

def scoring_B(datalist):
    share = find_index(datalist, "Shares Mil")
    
    if datalist[share][10] != "":
        share10 = float(datalist[share][10].replace(",", ""))
    else:
        share10 = 0

    if datalist[share][5] != "":
        share5 = float(datalist[share][5].replace(",", ""))
    else:
        share5 = 0

    if share10 < share5:
        return 1
    
    return 0

def scoring_I(datalist):
    pr = find_index(datalist, "Payout Ratio % *")
    years = 5
    
    pr_list = []
    for i in datalist[pr][11-years:11]:
        if i != "":
            pr_list.append(float(i.replace(",", "")))
        else:
            pr_list.append(0)
            
    if sum(pr_list)/len(pr_list) < 50:
        if pr_list[len(pr_list)-1] < 50:
            return 1

    if sum(pr_list)/len(pr_list) < 75:
        if pr_list[len(pr_list)-1] < 75:
            return 0.5

    return 0

def scoring_ROE(datalist):
    roe = find_index(datalist, "Return on Equity %")
    de = find_index(datalist, "Debt/Equity")

    roe_list = []
    for i in datalist[roe][1:11]:
        if i != "":
            roe_list.append(float(i.replace(",", "")))
        else:
            roe_list.append(0)

    if float(sum(roe_list)) / len(roe_list) > 15:
        if datalist[de][10] != "":
            if float(datalist[de][10]) < 1:
                return 1
        else:
            return 1

    return 0

def scoring_DEBT(datalist, marketCap):
    short = find_index(datalist, "Short-Term Debt")
    long = find_index(datalist, "Long-Term Debt")
    cash = find_index(datalist, "Cash & Short-Term Investments")

    if datalist[short][11] != "":
        short11 = float(datalist[short][11].replace(",", ""))
    else:
        short11 = 0

    if datalist[long][11] != "":
        long11 = float(datalist[long][11].replace(",", ""))
    else:
        long11 = 0

    if datalist[cash][11] != "":
        cash11 = float(datalist[cash][11].replace(",", ""))
    else:
        cash11 = 0

    dc = (short11 + long11 - cash11)/marketCap*1000000
    if dc < 0.2:
        return 1
    if dc < 0.5:
        return 0

    return -1

def scoring_S(beta):
    if beta < 1.2:
        return 1

    return 0

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

    DG = []
    F = []
    RVN = []
    EQ = []
    ER = []
    B = []
    I = []
    ROE = []
    DEBT = []
    S = []

    score = []
    ids = []

    for input in df_in['stock']:
        print(input)
        # --------------
        # gurufocus part
        # --------------
        url = "https://www.gurufocus.com/stock/" + input + "/dividend"

        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })
        try:
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")
        except:
            print("can't find {} on Gurufocus".format(input))
            continue
            
        soup = bs4.BeautifulSoup(data, "lxml")

        try:
            cut = soup.prettify().split("dividend_growth_5y:")[1]
            dividend_growth_5y = float(cut.split(",")[0])
        except:
            dividend_growth_5y = 0

        try:
            cut = soup.prettify().split(",dividend_growth_10y:")[1]
            dividend_growth_10y = float(cut.split(",")[0])
        except:
            dividend_growth_10y = 0

        # ----------
        # yahoo part
        # ----------
        url = "https://finance.yahoo.com/quote/" + input + "?p=" + input + "&.tsrc=fin-srch"

        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try:
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")
        except:
            print("can't find {} on Yahoo".format(input))
            continue
            
        soup = bs4.BeautifulSoup(data, "lxml")
        try:
            cut = soup.prettify().split(",\"beta\":{\"raw\":")[1]
            beta = float(cut.split(",")[0])
        except:
            beta = 2

        try:
            cut = soup.prettify().split(",\"marketCap\":{\"raw\":")[1]
            marketCap = float(cut.split(",")[0])
        except:
            marketCap = 1

        # --------
        # DGM part
        # --------
        stock = input.replace("/", ".")
        with open(".\\key_ratios\\{}\\{} Key Ratios.csv".format(category, stock), newline='',encoding="utf-8") as csvfile:
            rows = csv.reader(csvfile)
            datalist = list(rows)

            ids.append(stock)
            value = []
            value.append(scoring_DG(dividend_growth_5y))
            DG.append(value[0])
            value.append(scoring_F(datalist))
            F.append(value[1])
            value.append(scoring_RVN(datalist))
            RVN.append(value[2])
            value.append(scoring_EQ())
            EQ.append(value[3])
            value.append(scoring_ER(dividend_growth_5y, dividend_growth_10y))
            ER.append(value[4])
            value.append(scoring_B(datalist))
            B.append(value[5])
            value.append(scoring_I(datalist))
            I.append(value[6])
            value.append(scoring_ROE(datalist))
            ROE.append(value[7])
            value.append(scoring_DEBT(datalist, marketCap))
            DEBT.append(value[8])
            value.append(scoring_S(beta))
            S.append(value[9])
            score.append(sum(value))

        df_dic = {
            "Quality Score": score,
            'Dividend Growth Rate (5y)': DG,
            'FCF Payout Ratio': F,
            'Revenue and EPS': RVN,
            'Enterprice Quality': EQ,
            "Five/ten Ratio": ER,
            'Buybacks': B,
            'Income Payout Ratio': I,
            'ROE': ROE,
            "Debt": DEBT,
            'Stability': S
        }
        df_out = pd.DataFrame(data=df_dic, index=ids)
        df_out.to_csv(".\\scoring_DGM\\{}.csv".format(category))

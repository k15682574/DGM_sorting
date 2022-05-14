import numpy as np
import pandas as pd
import csv
import urllib.request as req
import bs4
import re
import pandas as pd
import numpy as np
import json
import time
import math

def find_index(datalist, key):
    for title in range(len(datalist)):
        try:
            if datalist[title][0] == key:
                return title
        except:
            continue
    
    return -1  

def scoring_DG(datalist):
    div = find_index(datalist, "Dividends USD")
    if datalist[div][5] != "" and datalist[div][10] != "":
        ratio = float(datalist[div][10].replace(",", "")) / float(datalist[div][5].replace(",", ""))
        dg5y = (math.pow(ratio, 1.0/5) - 1) * 100
    else:
        dg5y = 0
    if dg5y >= 10:
        return 1

    if dg5y >= 6:
        return 0.5

    return 0

def scoring_F(datalist):
    fcf_all = find_index(datalist, "Free Cash Flow USD Mil")
    share = find_index(datalist, "Shares Mil")
    div = find_index(datalist, "Dividends USD")
    years = 5
    
    share_list = []
    for i in datalist[share][11-years:11]:
        if i != "":
            share_list.append(float(i.replace(",", "")))
        else:
            share_list.append(0)

    fcf_all_list = []
    for i in datalist[fcf_all][11-years:11]:
        if i != "":
            fcf_all_list.append(float(i.replace(",", "")))
        else:
            fcf_all_list.append(0)

    """
    fcf_list = []
    for i in datalist[fcf][11-years:11]:
        if i != "":
            fcf_list.append(float(i.replace(",", "")))
        else:
            fcf_list.append(0)
    """

    fcf_list = []
    for i in range(len(fcf_all_list)):
        fcf_list.append(fcf_all_list[i]/share_list[i])

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

    if sum(fcf_payout_list)/len(fcf_payout_list) <= 0.4:
        if fcf_payout_list[len(fcf_payout_list)-1] <= 0.4:
            return 1

    if sum(fcf_payout_list)/len(fcf_payout_list) <= 0.75:
        if fcf_payout_list[len(fcf_payout_list)-1] <= 0.75:
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

def scoring_EQ(category):
    if category == "dividend_challenger":
        return 1
    if category == "dividend_contender":
        return 2
    if category == "dividend_champion":
        return 3
    if category == "dividend_king":
        return 4

    return 0

def scoring_ER(datalist):
    div = find_index(datalist, "Dividends USD")
    if datalist[div][10] != "" and datalist[div][5] != "":
        ratio_5 = float(datalist[div][10].replace(",", "")) / float(datalist[div][5].replace(",", ""))
        dg5y = (math.pow(ratio_5, 1.0/5) - 1) * 100
    else:
        dg5y = 0
    if datalist[div][10] != "" and datalist[div][1] != "":
        ratio_9 = float(datalist[div][10].replace(",", "")) / float(datalist[div][1].replace(",", ""))
        dg10y = (math.pow(ratio_9, 1.0/9) - 1) * 100
    else:
        dg10y = 0
    if dg10y >= 0:
        if dg5y >= dg10y:
            return 1

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
            
    if sum(pr_list)/len(pr_list) <= 50:
        if pr_list[len(pr_list)-1] <= 50:
            return 1

    if sum(pr_list)/len(pr_list) <= 75:
        if pr_list[len(pr_list)-1] <= 75:
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

    if float(sum(roe_list)) / len(roe_list) >= 15:
        if datalist[de][10] != "":
            if float(datalist[de][10]) <= 1:
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
    if dc <= 0.2:
        return 1
    if dc <= 0.5:
        return 0

    return -1

def scoring_S(beta):
    if beta <= 1.2:
        return 1

    return 0

def pricing_Y4(div, price):
    fair_price = price * div / 4
    if div >= 4:
        return 1, fair_price

    return 0, fair_price

def pricing_YSP500(div, price):
    fair_price = price * div / 1.97
    if div >= 1.97:
        return 1, fair_price
        
    return 0, fair_price

def pricing_C(div, datalist, price):
    div = find_index(datalist, "Dividends USD")
    if datalist[div][10] != "" and datalist[div][5] != "":
        ratio = float(datalist[div][10].replace(",", "")) / float(datalist[div][5].replace(",", ""))
        dg5y = (math.pow(ratio, 1.0/5) - 1) * 100
    else:
        dg5y = 0
    diff = 15 - dg5y - div
    if diff != 0:
        fair_price = price * div / diff
    else:
        fair_price = price

    if diff <= 0:
        return 1, price

    return 0, fair_price

def pricing_F(last_price, datalist):
    fcf = find_index(datalist, "Free Cash Flow Per Share * USD")
    fcf_all = find_index(datalist, "Free Cash Flow USD Mil")
    share = find_index(datalist, "Shares Mil")
    
    if datalist[fcf_all][10] != "":
        fcf_all_TTM = float(datalist[fcf_all][10].replace(",", ""))
    else:
        fcf_all_TTM = 0
        
    if datalist[share][10] != "":
        share_TTM = float(datalist[share][10].replace(",", ""))
    else:
        share_TTM = 0
    """
    if datalist[fcf][10] != "":
        fcf_TTM = float(datalist[fcf][10].replace(",", ""))
    else:
        fcf_TTM = 0
    """

    fcf_TTM = fcf_all_TTM/share_TTM
    fair_price = fcf_TTM / 0.05

    if fcf_TTM/last_price >= 0.1:
        return 2, fair_price

    if fcf_TTM/last_price >= 0.07:
        return 1.5, fair_price

    if fcf_TTM/last_price >= 0.05:
        return 1, fair_price

    return 0, fair_price

def pricing_PE(pe_ratio_now, price):
    if pe_ratio_now != 0:
        fair_price = price / pe_ratio_now * 15
    else:
        fair_price = 0

    if pe_ratio_now <= 15 and pe_ratio_now != 0:
        return 1, fair_price

    return 0, fair_price

def pricing_R(pe_ratio_now, datalist):
    roe = find_index(datalist, "Return on Equity %")
    de = find_index(datalist, "Debt/Equity")

    roe_list = []
    for i in datalist[roe][1:11]:
        if i != "":
            roe_list.append(float(i.replace(",", "")))
        else:
            roe_list.append(0)

    if pe_ratio_now <= 15:
        if float(sum(roe_list)) / len(roe_list) >= 20:
            if datalist[de][10] != "":
                if float(datalist[de][10]) <= 1:
                    return 1
            else:
                return 1

    return 0

def pricing_TD(div, div_avg, price):
    if div_avg != 0:
        fair_price = price * div / div_avg
    else:
        fair_price = price

    if div >= div_avg:
        return 1, fair_price

    return 0, fair_price

def pricing_TP(pe_ratio_now, pe_ratio_avg, price):
    if pe_ratio_now * pe_ratio_avg != 0:
        fair_price = price / pe_ratio_now * pe_ratio_avg
    else:
        fair_price = 0

    if pe_ratio_now <= pe_ratio_avg and pe_ratio_now != 0:
        return 1, fair_price

    return 0, fair_price

def pricing_D(last_price, datalist):
    div = find_index(datalist, "Dividends USD")
    if datalist[div][10] != "" and datalist[div][5] != "":
        ratio = float(datalist[div][10].replace(",", "")) / float(datalist[div][5].replace(",", ""))
        dg5y = (math.pow(ratio, 1.0/5) - 1) * 100
    else:
        dg5y = 0
    div = find_index(datalist, "Dividends USD")
    if datalist[div][10] != "":
        last_div = float(datalist[div][10].replace(",", ""))
    else:
        last_div = 0
    
    if dg5y/100 >= 0.12:
        return 1, last_price

    ddm = last_div * (1 + dg5y/100) / (0.12 - dg5y/100)

    if last_price <= ddm:
        return 1, ddm

    return 0, ddm

def pricing_PS(PFScore):
    if PFScore > 5:
        return 1

    return 0

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
    p_Y4 = []
    p_YSP500 = []
    p_C = []
    p_F = []
    p_PE = []
    p_R = []
    p_TD = []
    p_TP = []
    p_D = []
    p_PS = []

    score = []
    pricing = []
    final_fair = []
    ratio_to_fair = []
    ids = []

    for input in df_in['stock']:
        try_max = 5
        print(input)

        # --------------
        # gurufocus part
        # --------------
        url = "https://www.gurufocus.com/stock/" + input + "/dividend"

        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try_cnt = 0
        while try_cnt < try_max:
            try:
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8")

                soup = bs4.BeautifulSoup(data, "lxml")
                break
            except:
                print("can't find {} dividend growth on Gurufocus".format(input))
                try_cnt += 1

        try:
            cut = soup.prettify().split("dividend_growth_5y:")[1]
            dividend_growth_5y = float(cut.split(",")[0])
        except:
            dividend_growth_5y = 0

        # print(f'{input} dividend_growth_5y = {dividend_growth_5y}')

        try:
            cut = soup.prettify().split(",dividend_growth_10y:")[1]
            dividend_growth_10y = float(cut.split(",")[0])
        except:
            dividend_growth_10y = 0

        # print(f'{input} dividend_growth_10y = {dividend_growth_10y}')

        url = "https://www.gurufocus.com/stock/" + input + "/summary?position=back-to-top"
        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try_cnt = 0
        while try_cnt < try_max:
            try:
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8")

                soup = bs4.BeautifulSoup(data, "lxml")
                break
            except:
                print("can't find {} Piotroski F-Score on Gurufocus".format(input))
                try_cnt += 1

        try:
            element = soup.find_all('a', {'href': re.compile("(.*)(Piotroski-F-Score)(.*)")})
            # print(element)
            
            # Extracting the next sibling of parent
            nextSibling = element[1].find_next_sibling("span")
            # print(nextSibling)

            # Extracting the next sibling of parent
            text = nextSibling.getText()
            # print(text)

            PFScore = int(text.replace("/9", ""))
            
        except:
            PFScore = 0

        # print(f'{input} PFScore is {PFScore} out')

        # ----------
        # yahoo part
        # ----------
        url = "https://finance.yahoo.com/quote/" + input + "?p=" + input + "&.tsrc=fin-srch"

        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try_cnt = 0
        while try_cnt < try_max:
            try:
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8")

                soup = bs4.BeautifulSoup(data, "lxml")
                break
            except:
                print("can't find {} on Yahoo".format(input))
                try_cnt += 1

        try:
            cut = soup.prettify().split(",\"beta\":{\"raw\":")[1]
            beta = float(cut.split(",")[0])
        except:
            beta = 2

        # print(f'{input} beta = {beta}')

        try:
            cut = soup.prettify().split(",\"marketCap\":{\"raw\":")[1]
            marketCap = float(cut.split(",")[0])
        except:
            marketCap = 1

        # print(f'{input} marketCap = {marketCap}')

        # -----------------
        # seekingalpha part
        # -----------------
        
        url = "https://finance.api.seekingalpha.com/v2/real-time-prices?symbols=" + input
        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try_cnt = 0
        while try_cnt < try_max:
            try:
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8") # .json format

                data = json.loads(data)
                break
            except:
                print("can't find {} price on SeekingAlpha".format(input))
                try_cnt += 1

        try:
            last_price = data["data"][0]["attributes"]["last"]
        except:
            last_price = 0

        # print(f'{input} last price = {last_price}')
        
        # -----------------
        # ycharts part
        # -----------------
        url = "https://ycharts.com/companies/" + input + "/pe_ratio"

        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try_cnt = 0
        while try_cnt < try_max:
            try:
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8")

                soup = bs4.BeautifulSoup(data, "lxml")
                break
            except:
                print("can't find {} pe ratio on ycharts".format(input))
                try_cnt += 1

        try:
            cut = soup.prettify().split("<span class=\"page-name-date\">")[1]
            pe_ratio_now = float(cut.split("for ")[0].replace(" ", ""))
        except:
            pe_ratio_now = 0
        
        # print(f'{input} pe_ratio_now = {pe_ratio_now}')
        
        try:
            cut = soup.prettify().split("Maximum")[1]
            cut = cut.split("Average")[0]
            cut = cut.split("<div class=\"key-stat-title\">")[1]
            temp = cut.split("</div>")[0]
            temp = temp.replace("\t", "")
            temp = temp.replace("\n", "")
            temp = temp.replace(" ", "")
            pe_ratio_avg = float(temp)

        except:
            pe_ratio_avg = 0

        # print(f'{input} pe_ratio_avg = {pe_ratio_avg}')

        url = "https://ycharts.com/companies/" + input + "/dividend_yield"

        request = req.Request(url, headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        })

        try_cnt = 0
        while try_cnt < try_max:
            try:
                with req.urlopen(request) as response:
                    data = response.read().decode("utf-8")

                soup = bs4.BeautifulSoup(data, "lxml")
                break
            except:
                print("can't find {} dividend yield on ycharts".format(input))
                try_cnt += 1

        try:
            cut = soup.prettify().split("<span class=\"page-name-date\">")[1]
            dividend_yield = float(cut.split("%")[0].replace(" ", ""))
        except:
            dividend_yield = 0
        
        # print(f'{input} dividend_yield = {dividend_yield}')
        
        try:
            cut = soup.prettify().split("Maximum")[1]
            cut = cut.split("Average")[0]
            cut = cut.split("<div class=\"key-stat-title\">")[1]
            temp = cut.split("%")[0]
            temp = temp.replace("\t", "")
            temp = temp.replace("\n", "")
            temp = temp.replace(" ", "")
            dividend_yield_4y_avg = float(temp)

        except:
            dividend_yield_4y_avg = 0

        # print(f'{input} dividend_yield_4y_avg = {dividend_yield_4y_avg}')

        # --------
        # DGM part
        # --------
        stock = input.replace("/", ".")
        with open(".\\key_ratios\\{} Key Ratios.csv".format(stock), newline='',encoding="utf-8") as csvfile:
            rows = csv.reader(csvfile)
            datalist = list(rows)

            ids.append(stock)
            value_s = []
            value_s.append(scoring_DG(datalist))
            DG.append(value_s[0])
            value_s.append(scoring_F(datalist))
            F.append(value_s[1])
            value_s.append(scoring_RVN(datalist))
            RVN.append(value_s[2])
            value_s.append(scoring_EQ(category))
            EQ.append(value_s[3])
            value_s.append(scoring_ER(datalist))
            ER.append(value_s[4])
            value_s.append(scoring_B(datalist))
            B.append(value_s[5])
            value_s.append(scoring_I(datalist))
            I.append(value_s[6])
            value_s.append(scoring_ROE(datalist))
            ROE.append(value_s[7])
            value_s.append(scoring_DEBT(datalist, marketCap))
            DEBT.append(value_s[8])
            value_s.append(scoring_S(beta))
            S.append(value_s[9])
            score.append(sum(value_s))

            value_p = []
            fair = []

            point, fair_price = pricing_Y4(dividend_yield, last_price)
            value_p.append(point)
            fair.append(fair_price)
            p_Y4.append(value_p[0])

            point, fair_price = pricing_YSP500(dividend_yield, last_price)
            value_p.append(point)
            fair.append(fair_price)
            p_YSP500.append(value_p[1])

            point, fair_price = pricing_C(dividend_yield, datalist, last_price)
            value_p.append(point)
            fair.append(fair_price)
            p_C.append(value_p[2])

            point, fair_price = pricing_F(last_price, datalist)
            value_p.append(point)
            fair.append(fair_price)
            fair.append(fair_price/2)
            p_F.append(value_p[3])

            point, fair_price = pricing_PE(pe_ratio_now, last_price)
            value_p.append(point)
            fair.append(fair_price)
            p_PE.append(value_p[4])

            value_p.append(pricing_R(pe_ratio_now, datalist))
            p_R.append(value_p[5])

            point, fair_price = pricing_TD(dividend_yield, dividend_yield_4y_avg, last_price)
            value_p.append(point)
            fair.append(fair_price)
            p_TD.append(value_p[6])

            point, fair_price = pricing_TP(pe_ratio_now, pe_ratio_avg, last_price)
            value_p.append(point)
            fair.append(fair_price)
            p_TP.append(value_p[7])

            point, fair_price = pricing_D(last_price, datalist)
            value_p.append(point)
            fair.append(fair_price)
            p_D.append(value_p[8])

            value_p.append(pricing_PS(PFScore))
            p_PS.append(value_p[9])

            pricing.append(sum(value_p))

            fair_sorted = sorted(fair, reverse=True)
            final_fair.append(fair_sorted[6 - int(value_p[9] + value_p[5])])

            if (fair_sorted[6 - int(value_p[9] + value_p[5])]) != 0:
                ratio_to_fair.append(last_price / (fair_sorted[6 - int(value_p[9] + value_p[5])]))
            else:
                ratio_to_fair.append(100)

        # print(input, fair, fair_sorted)
        df_dic = {
            "Quality Score": score,
            "Pricing Score": pricing,
            "Fair Price": final_fair,
            "Ratio To Fair Price": ratio_to_fair,
            'Dividend Growth Rate (5y)': DG,
            'FCF Payout Ratio': F,
            'Revenue and EPS': RVN,
            'Enterprice Quality': EQ,
            "Five/ten Ratio": ER,
            'Buybacks': B,
            'Income Payout Ratio': I,
            'ROE': ROE,
            "Debt": DEBT,
            'Stability': S,
            'Yield > 4%': p_Y4,
            'Yield > S&P500': p_YSP500,
            'Chowder > 15': p_C,
            'FCF Yield > 5%': p_F,
            'PE < 15': p_PE,
            'ROE > 20% + PE < 15': p_R,
            'Target Dividend Yield': p_TD,
            'Target PE': p_TP,
            'DDM Value': p_D,
            'Piotroski-F Score': p_PS
        }
        df_out = pd.DataFrame(data=df_dic, index=ids)
        df_out.to_csv(".\\scoring_DGM\\{}.csv".format(category))

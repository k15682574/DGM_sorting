import urllib.request as req
import bs4
import re
import pandas as pd
import numpy as np

df_in = pd.read_csv('./DGM_challenger.csv')
np_in = df_in.values
print(np_in)
print(type(np_in))
np_out = np.zeros(shape=(df_in.shape[0], 7))
#np_out[:, 0] = np_in[:, 0]
columns_name = ["dividend_growth_5y", "dividend_growth_10y", "beta", "DG", "E1", "E2", "S"]
rows_name = df_in['company']
index = 0
for i in df_in['company']:

	# gurufocus start
	url = "https://www.gurufocus.com/stock/" + i + "/dividend"

	request = req.Request(url, headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
	})

	with req.urlopen(request) as response:
		data = response.read().decode("utf-8")
		
	soup = bs4.BeautifulSoup(data, "lxml")

	cut = soup.prettify().split("dividend_growth_5y:")[1]
	if cut.split(",")[0] != 'a' and cut.split(",")[0] != 'ax':
		dividend_growth_5y = float(cut.split(",")[0])

	print("dividend_growth_5y is", dividend_growth_5y)
	np_out[index][0] = dividend_growth_5y
	'''
	cut = soup.prettify().split(",yield:")[2]
	dividend_yield = float(cut.split(",")[0])
	print("dividend_yield is", dividend_yield)
	'''
	cut = soup.prettify().split(",dividend_growth_10y:")[1]
	dividend_growth_10y = 0
	if cut.split(",")[0] != 'a' and cut.split(",")[0] != 'ax':
		dividend_growth_10y = float(cut.split(",")[0])
	print("dividend_growth_10y is", dividend_growth_10y)
	np_out[index][1] = dividend_growth_10y
	'''
	url = "https://www.gurufocus.com/stock/" + i + "/summary"

	request = req.Request(url, headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
	})

	with req.urlopen(request) as response:
		data = response.read().decode("utf-8")
		
	soup = bs4.BeautifulSoup(data, "lxml")
	
	cut = soup.prettify().split("Piotroski F-Score\n</a></td> <td data-v-d8b0497c> ")[1]
	print(cut)
	Piotroski_F_Score = float(cut.split(" ")[0])
	print("Piotroski_F_Score is", Piotroski_F_Score)
	'''
	# gurufocus end

	# yahoo start
	url = "https://finance.yahoo.com/quote/" + i + "?p=" + i + "&.tsrc=fin-srch"

	request = req.Request(url, headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
	})

	with req.urlopen(request) as response:
		data = response.read().decode("utf-8")
		
	soup = bs4.BeautifulSoup(data, "lxml")

	cut = soup.prettify().split(",\"beta\":{")[1]
	cut = cut.split("\"fmt\":\"")[1]
	beta = float(cut.split("\"},")[0])
	print("beta is", beta)
	np_out[index][2] = beta
	# yahoo end
	'''
	# morningstar start
	url = "https://www.morningstar.com/stocks/xnys/hd/quote"

	request = req.Request(url, headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
	})

	with req.urlopen(request) as response:
		data = response.read().decode("utf-8")
		
	soup = bs4.BeautifulSoup(data, "lxml")

	cut = soup.prettify().split(",\"beta\":{")[1]
	cut = cut.split("\"fmt\":\"")[1]
	beta = float(cut.split("\"},")[0])
	print("beta is", beta)
	# morningstar end
	'''
	
	if dividend_growth_5y > 10:
		np_out[index][3] = 1
	elif dividend_growth_5y > 6:
		np_out[index][3] = 0.5
	else:
		np_out[index][3] = 0

	if dividend_growth_5y >= dividend_growth_10y and dividend_growth_10y != 0:
		np_out[index][5] = 1
	else:
		np_out[index][5] = 0

	if float(np_in[index, 2]) >= 50:
		np_out[index][4] = 4
	elif float(np_in[index, 2]) >= 25:
		np_out[index][4] = 3
	elif float(np_in[index, 2]) >= 10:
		np_out[index][4] = 2
	elif float(np_in[index, 2]) >= 5:
		np_out[index][4] = 1
	else:
		np_out[index][4] = 0

	if beta < 1.2:
		np_out[index][6] = 1
	else:
		np_out[index][6] = 0

	print(np_out[index, :])
	index = index + 1
	
df_out = pd.DataFrame(np_out, index=rows_name, columns=columns_name)
df_out.to_csv("DGM_challenger_check.csv", index=0)
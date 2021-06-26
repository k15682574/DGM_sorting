import urllib.request as req
import bs4
import re

# gurufocus start
url = "https://www.gurufocus.com/stock/hd/dividend"

request = req.Request(url, headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
})

with req.urlopen(request) as response:
	data = response.read().decode("utf-8")
	
soup = bs4.BeautifulSoup(data, "lxml")

cut = soup.prettify().split("dividend_growth_5y:")[1]
dividend_growth_5y = float(cut.split(",")[0])
print("dividend_growth_5y is", dividend_growth_5y)

cut = soup.prettify().split(",yield:")[2]
dividend_yield = float(cut.split(",")[0])
print("dividend_yield is", dividend_yield)

cut = soup.prettify().split(",dividend_growth_10y:")[1]
dividend_growth_10y = 0
if cut.split(",")[0] != 'a':
	dividend_growth_10y = float(cut.split(",")[0])
print("dividend_growth_10y is", dividend_growth_10y)
# gurufocus end

# yahoo start
url = "https://finance.yahoo.com/quote/HD?p=HD&.tsrc=fin-srch"

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
# yahoo end

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

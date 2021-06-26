import urllib.request as req
import bs4
import re
url = "https://www.gurufocus.com/stock/abbv/dividend"

request = req.Request(url, headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
})

with req.urlopen(request) as response:
	data = response.read().decode("utf-8")
	
soup = bs4.BeautifulSoup(data, "lxml")
'''
target = soup.find("script", text = re.compile("dividend_growth_5y"))
cut1 = target.prettify().split("dividend_growth_5y:")
cut2 = float(cut1[1].split(",")[0])
'''
cut1 = soup.prettify().split("dividend_growth_5y:")[1]
cut2 = float(cut1.split(",")[0])
print(cut2)
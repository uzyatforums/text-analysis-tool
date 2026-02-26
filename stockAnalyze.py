from datetime import datetime
import yfinance as yf
import requests



def extractBasicInfo(data):
    keyToExtract = [
        'longName',
        'website',
        'sector',
        'fullTimeEmployees',
        'marketCap',
        'totalRevenue',
        'trailingEps',
    ]
    basicInfo = {}
    for key in keyToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ''
    return basicInfo


def getPriceHistory(company):
    historyDF = company.history(period='12mo')
    prices = historyDF['Open'].tolist()
    dates = historyDF.index.strftime('%Y-%m-%d').tolist()
    return {'price': prices, 'date': dates}


def getEarningsDates(company):
    earningsDateDf = company.earnings_dates
    allDates = earningsDateDf.index.strftime('%Y-%m-%d').tolist()
    dateObjects = [datetime.strptime(date, '%Y-%m-%d') for date in allDates]
    currentDate = datetime.now()
    futureDates = [
        date.strftime('%Y-%m-%d') for date in dateObjects if date > currentDate
    ]
    return futureDates


def getCompanyNews(company):
    newsList = company.news
    allNewsArticles = []
    for newsDict in newsList:
        newsDictToAdd = {'title': newsDict.get('title'), 'link': newsDict.get('link')}
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extractCompanyNewsArticles(newsArticles):
    # url = newsArticles[0]['link']
    url = 'https://finance.yahoo.com/news/the-ai-spending-boom-is-creating-winners-beyond-the-mag-7-why-one-sector-could-see-big-gains-153820672.html'
    page = requests.get(url, headers=headers)
    print(page.text)


def getCompanyStockInfo(tickerSymbol):
    # Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticles = getCompanyNews(company)
    extractCompanyNewsArticles(newsArticles)

getCompanyStockInfo('MSFT')

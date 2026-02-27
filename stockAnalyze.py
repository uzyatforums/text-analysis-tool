from datetime import datetime
import yfinance as yf
import requests
import pprint
import json
from bs4 import BeautifulSoup

def extractBasicInfo(data):
    keyToExtract = [
        "longName",
        "website",
        "sector",
        "fullTimeEmployees",
        "marketCap",
        "totalRevenue",
        "trailingEps",
    ]
    basicInfo = {}
    for key in keyToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ""
    return basicInfo


def getPriceHistory(company):
    historyDF = company.history(period="12mo")
    prices = historyDF["Open"].tolist()
    dates = historyDF.index.strftime("%Y-%m-%d").tolist()
    return {"price": prices, "date": dates}


def getEarningsDates(company):
    earningsDateDf = company.earnings_dates
    allDates = earningsDateDf.index.strftime("%Y-%m-%d").tolist()
    dateObjects = [datetime.strptime(date, "%Y-%m-%d") for date in allDates]
    currentDate = datetime.now()
    futureDates = [
        date.strftime("%Y-%m-%d") for date in dateObjects if date > currentDate
    ]
    return futureDates


# def getCompanyNews(company):
#     newsList = company.news
#     allNewsArticles = []
#     for newsDict in newsList:
#         newsDictToAdd = {'title': newsDict.get('title'), 'link': newsDict.get('link')}
#         allNewsArticles.append(newsDictToAdd)
#     return allNewsArticles

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def extractCompanyNewsArticles(newsArticles):
    for newsArticle in newsArticles:
        url = newsArticle["url"]
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        if(soup.find_all(string="Story continues")):
            print("Tag found - should skip")
        else:
            print("Tag not found, don't skip")

def getCompanyNews(company):
    news_items = company.news
    articles = []

    if not news_items:
        return []

    for item in news_items:
        content = item.get("content", {})

        # Only keep real articles (not videos)
        if content.get("contentType") != "STORY":
            continue

        title = content.get("title")
        pub_date = content.get("pubDate")

        canonical = content.get("canonicalUrl", {})
        url = canonical.get("url")

        if title and url:
            articles.append({"title": title, "url": url, "published": pub_date})

    # print(json.dumps(articles, indent=2))
    return articles


def getCompanyStockInfo(tickerSymbol):
    # Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)

    # Get news about company
    newsArticles = getCompanyNews(company)
    extractCompanyNewsArticles(newsArticles)


getCompanyStockInfo("AAPL")

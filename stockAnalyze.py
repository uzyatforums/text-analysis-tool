from datetime import datetime
from matplotlib.pyplot import title
import yfinance as yf
import requests
import pprint
import json
from bs4 import BeautifulSoup
import analyze



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

def extractNewwArticlesTextFromHtml(soup):
    allText = ""
    result = soup.find("div", {"data-testid": "article-body"}) or soup.find(
        "div", class_="caas-body"
    )
    print(result)
    # exit("sssssss")
    for res in result:
        allText += res.text
    return allText

headers = {"User-Agent": "Mozilla/5.0"}

def extract_yahoo_article(url):

    # Only process Yahoo-hosted articles
    # Yahoo does block requests for external articles, so we skip those to avoid unnecessary errors
    if "yahoo.com" not in url:
        return ""

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Skipping URL due to request error: {url}")
        print("Reason:", e)
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # ---- Extract title from meta ----
    meta_title = soup.find("meta", attrs={"name": "title"})
    title = meta_title.get("content") if meta_title else "No Title Found"

    # ---- Extract article body ----
    body_div = (
        soup.find("div", {"data-testid": "article-body"})
        or soup.find("div", class_="caas-body")
    )

    if not body_div:
        print(f"Article body not found for: {url}")
        return f"{title}\n\n"

    paragraphs = body_div.find_all("p")
    article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

    # Return formatted text
    return f"{title}\n\n{article_text}\n\n{'-'*80}\n\n"

def extractCompanyNewsArticles(newsArticles):
    allArticlesText = ""
    for newsArticle in newsArticles:
        url = newsArticle["url"]
        allArticlesText += extract_yahoo_article(url)
            
    return allArticlesText


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

    # Check if company exists, if not trigger error
    if not basicInfo["longName"]:
        raise NameError('Could not find stock info, symbol may be delisted or does not exist')  
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)

    # Get company news
    newsArticles = getCompanyNews(company)
    # print(json.dumps(newsArticles, indent=2))
    newsArticlesAllText = extractCompanyNewsArticles(newsArticles)
    newsTextAnalysis = analyze.analyzeText(newsArticlesAllText)

    finalStockAnalysis = {
        "basicInfo": basicInfo,
        "priceHistory": priceHistory,
        "futureEarningsDates": futureEarningsDates,
        "newsArticles": newsArticles,
        "newsTextAnalysis": newsTextAnalysis
    }   
    return finalStockAnalysis

# companyStockAnalysis = getCompanyStockInfo("MSFT")
# print(json.dumps(companyStockAnalysis, indent=4))

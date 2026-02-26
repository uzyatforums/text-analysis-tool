import yfinance as yf

def extractBasicInfo(data):
    keyToExtract = ["longName", "website", "sector", "fullTimeEmployees", "marketCap", "totalRevenue", "trailingEps"]  
    basicInfo = {}
    for key in keyToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ""
    return basicInfo
    

def getCompanyStockInfo(tickerSymbol):
    company = yf.Ticker(tickerSymbol)
    basicInfo = extractBasicInfo(company.info)
    print(basicInfo)


getCompanyStockInfo("MSFT")
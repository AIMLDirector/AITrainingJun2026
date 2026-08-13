import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker="AAPL"):
    stock = yf.Ticker(ticker)

    hist = stock.history(period="1y")
    info = stock.info

    financials = {
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "marketCap": info.get("marketCap"),
        "currentPrice": info.get("currentPrice"),
        "peRatio": info.get("trailingPE"),
        "eps": info.get("trailingEps"),
        "revenueGrowth": info.get("revenueGrowth")
    }

    return hist, financials
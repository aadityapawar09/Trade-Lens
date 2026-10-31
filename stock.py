import yfinance as yf


def get_stock_data(symbol):
    # Ask Yahoo Finance for information about the stock
    try:
        info = yf.Ticker(symbol).info
    except Exception:
        return None  # something went wrong (no internet, bad symbol, etc.)

    # Some stocks use "currentPrice", others use "regularMarketPrice"
    price = info.get("currentPrice") or info.get("regularMarketPrice")

    # Make big numbers easier to read: 1000000 becomes "1,000,000"
    market_cap = info.get("marketCap")
    if market_cap:
        market_cap = format(market_cap, ",")
    else:
        market_cap = "N/A"

    # Put everything in a dictionary (a box of label -> value pairs)
    return {
        "Company": info.get("longName", symbol),
        "Symbol": symbol,
        "Sector": info.get("sector", "N/A"),
        "Price": price,
        "Currency": info.get("currency", ""),
        "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
        "PE Ratio": info.get("trailingPE", "N/A"),
        "Market Cap": market_cap,
    }

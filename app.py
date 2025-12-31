import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Retail Radar", layout="wide")

st.title("📈 Retail Radar — Trending Stocks")

TICKERS = [
    "AAPL","TSLA","NVDA","AMD","PLTR",
    "SOFI","AMC","GME","META","MSFT"
]

def scan_stock(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="7d")

    if hist.empty:
        return None

    avg_vol = hist["Volume"].mean()
    last_vol = hist["Volume"][-1]
    vol_spike = last_vol / avg_vol

    price_change = (hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0]

    score = round(vol_spike * 50 + price_change * 100, 2)

    return {
        "Ticker": ticker,
        "Price": round(hist["Close"][-1], 2),
        "Change %": round(price_change * 100, 2),
        "Volume Spike": round(vol_spike, 2),
        "Popularity Score": score
    }

data = []
for t in TICKERS:
    d = scan_stock(t)
    if d:
        data.append(d)

df = pd.DataFrame(data).sort_values("Popularity Score", ascending=False)

st.subheader("🔥 Retail Momentum Rankings")
st.dataframe(df, use_container_width=True)

choice = st.selectbox("View stock chart", df["Ticker"])
chart = yf.Ticker(choice).history(period="1mo")
st.line_chart(chart["Close"])

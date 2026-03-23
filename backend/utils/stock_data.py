"""
Stock data fetching and technical indicator computation using yfinance.
"""

import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import yfinance as yf  # type: ignore
from datetime import date

START_DATE = "2015-01-01"

def get_today():
    return date.today().strftime("%Y-%m-%d")

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """Download OHLCV data from Yahoo Finance and compute technical indicators."""
    data = yf.download(ticker, START_DATE, get_today(), progress=False)

    # Flatten MultiIndex columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.reset_index(inplace=True)

    # Convert Date to string for JSON serialisation
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

    # Technical indicators
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    data["Vol_MA20"] = data["Volume"].rolling(20).mean()

    # Daily returns
    data["Daily_Return"] = data["Close"].pct_change() * 100

    # RSI (14-period)
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # Bollinger Bands (20-period)
    data["BB_Mid"] = data["Close"].rolling(20).mean()
    bb_std = data["Close"].rolling(20).std()
    data["BB_Upper"] = data["BB_Mid"] + 2 * bb_std
    data["BB_Lower"] = data["BB_Mid"] - 2 * bb_std

    # MACD
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = ema12 - ema26
    data["MACD_Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()
    data["MACD_Hist"] = data["MACD"] - data["MACD_Signal"]

    # Replace NaN with None for clean JSON
    data = data.replace({np.nan: None})

    return data

def get_stock_summary(data: pd.DataFrame) -> dict:
    """Compute summary statistics from stock data."""
    closes = [c for c in data["Close"].tolist() if c is not None]
    volumes = [v for v in data["Volume"].tolist() if v is not None]

    current_price = closes[-1] if closes else 0
    prev_price = closes[-2] if len(closes) > 1 else current_price
    change_pct = ((current_price - prev_price) / prev_price * 100) if prev_price else 0
    high_price = max(closes) if closes else 0
    low_price = min(closes) if closes else 0
    avg_volume = sum(volumes) / len(volumes) if volumes else 0

    # MA signals
    ma50_vals = [v for v in data["MA50"].tolist() if v is not None]
    ma200_vals = [v for v in data["MA200"].tolist() if v is not None]
    ma_signal = None
    if ma50_vals and ma200_vals:
        ma_signal = "golden_cross" if ma50_vals[-1] > ma200_vals[-1] else "death_cross"

    # RSI signal
    rsi_vals = [v for v in data["RSI"].tolist() if v is not None]
    latest_rsi = rsi_vals[-1] if rsi_vals else None

    return {
        "current_price": round(float(current_price), 2),  # pyre-ignore[6]
        "prev_price": round(float(prev_price), 2),  # pyre-ignore[6]
        "change_pct": round(float(change_pct), 2),  # pyre-ignore[6]
        "high_price": round(float(high_price), 2),  # pyre-ignore[6]
        "low_price": round(float(low_price), 2),  # pyre-ignore[6]
        "avg_volume": round(float(avg_volume), 0),  # pyre-ignore[6]
        "ma_signal": ma_signal,
        "latest_rsi": round(float(latest_rsi), 2) if latest_rsi else None,  # pyre-ignore[6]
        "data_points": len(closes),
    }

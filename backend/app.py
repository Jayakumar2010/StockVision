"""
StockVision Flask API Server
Serves stock data, technical indicators, and Prophet forecasts.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import traceback

from utils.stock_data import fetch_stock_data, get_stock_summary
from utils.forecaster import train_and_forecast

app = Flask(__name__)
CORS(app)

SUPPORTED_STOCKS = ["GOOG", "AAPL", "MSFT", "AMZN", "TSLA", "META", "NFLX", "NVDA", "GME"]

# ── Stock data ─────────────────────────────────────────────
@app.route("/api/stocks", methods=["GET"])
def list_stocks():
    """Return the list of supported stock tickers."""
    return jsonify({"stocks": SUPPORTED_STOCKS})


@app.route("/api/stock/<ticker>", methods=["GET"])
def get_stock(ticker):
    """Return historical OHLCV data with technical indicators."""
    ticker = ticker.upper()
    if ticker not in SUPPORTED_STOCKS:
        return jsonify({"error": f"Unsupported ticker: {ticker}"}), 400

    try:
        data = fetch_stock_data(ticker)
        summary = get_stock_summary(data)
        records = data.to_dict(orient="records")

        return jsonify({
            "ticker": ticker,
            "summary": summary,
            "data": records,
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ── Forecast ───────────────────────────────────────────────
@app.route("/api/forecast/<ticker>", methods=["GET"])
def get_forecast(ticker):
    """Return Prophet forecast for the given ticker."""
    ticker = ticker.upper()
    if ticker not in SUPPORTED_STOCKS:
        return jsonify({"error": f"Unsupported ticker: {ticker}"}), 400

    years = request.args.get("years", 2, type=int)
    years = max(1, min(years, 4))  # clamp to 1–4

    try:
        data = fetch_stock_data(ticker)
        result = train_and_forecast(data, years=years)

        return jsonify({
            "ticker": ticker,
            "years": years,
            **result,
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ── Market status ──────────────────────────────────────────
@app.route("/api/market-status", methods=["GET"])
def market_status():
    """Return whether the US stock market is approximately open."""
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    is_open = weekday < 5 and 9 <= hour < 16

    return jsonify({
        "is_open": is_open,
        "checked_at": now.strftime("%Y-%m-%d %H:%M:%S"),
    })


# ── Health ─────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("StockVision API Server starting on http://localhost:5000")
    app.run(debug=True, port=5000)

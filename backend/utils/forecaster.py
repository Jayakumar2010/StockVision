"""
Prophet-based stock price forecasting with caching.
"""

import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from prophet import Prophet  # type: ignore

# Simple in-memory cache
_model_cache = {}

def train_and_forecast(data: pd.DataFrame, years: int = 2) -> dict:
    """
    Train a Prophet model on historical closing prices and produce a forecast.

    Parameters
    ----------
    data : pd.DataFrame
        Must contain 'Date' (str YYYY-MM-DD) and 'Close' (float) columns.
    years : int
        Number of years to forecast ahead.

    Returns
    -------
    dict with keys:
        - forecast: list of dicts with ds, yhat, yhat_lower, yhat_upper
        - components: dict with trend & seasonality data
        - summary: dict with predicted price, growth %, bands
    """
    periods = years * 365

    df_train = data[["Date", "Close"]].copy()
    df_train.columns = ["ds", "y"]
    df_train["ds"] = pd.to_datetime(df_train["ds"])
    df_train["y"] = pd.to_numeric(df_train["y"], errors="coerce")
    df_train = df_train.dropna()

    # Train model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
    )
    model.fit(df_train)

    # Forecast
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Build forecast records
    forecast_records = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    forecast_records["ds"] = forecast_records["ds"].dt.strftime("%Y-%m-%d")
    forecast_list = forecast_records.to_dict(orient="records")

    # Trend component
    trend_records = forecast[["ds", "trend"]].copy()
    trend_records["ds"] = trend_records["ds"].dt.strftime("%Y-%m-%d")
    trend_list = trend_records.to_dict(orient="records")

    # Weekly seasonality
    weekly = None
    if "weekly" in forecast.columns:
        weekly_records = forecast[["ds", "weekly"]].copy()
        weekly_records["ds"] = weekly_records["ds"].dt.strftime("%Y-%m-%d")
        weekly = weekly_records.to_dict(orient="records")

    # Yearly seasonality
    yearly = None
    if "yearly" in forecast.columns:
        yearly_records = forecast[["ds", "yearly"]].copy()
        yearly_records["ds"] = yearly_records["ds"].dt.strftime("%Y-%m-%d")
        yearly = yearly_records.to_dict(orient="records")

    # Summary statistics
    current_price = float(df_train["y"].iloc[-1])
    forecast_latest = float(forecast["yhat"].iloc[-1])
    forecast_mean = float(forecast["yhat"].mean())
    forecast_high = float(forecast["yhat_upper"].max())
    forecast_low = float(forecast["yhat_lower"].min())
    price_growth = ((forecast_latest - current_price) / current_price * 100) if current_price else 0

    summary = {
        "current_price": round(float(current_price), 2),  # pyre-ignore[6]
        "predicted_price": round(float(forecast_latest), 2),  # pyre-ignore[6]
        "mean_forecast": round(float(forecast_mean), 2),  # pyre-ignore[6]
        "upper_band": round(float(forecast_high), 2),  # pyre-ignore[6]
        "lower_band": round(float(forecast_low), 2),  # pyre-ignore[6]
        "growth_pct": round(float(price_growth), 1),  # pyre-ignore[6]
        "years": years,
    }

    return {
        "forecast": forecast_list,
        "components": {
            "trend": trend_list,
            "weekly": weekly,
            "yearly": yearly,
        },
        "summary": summary,
    }

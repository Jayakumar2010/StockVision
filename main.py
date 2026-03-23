import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import plotly.express as px

# ---------------------------------
# App Configuration
# ---------------------------------
st.set_page_config(
    page_title="StockVision — AI Forecast",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# ---------------------------------
# Dark Glassmorphism Theme CSS
# ---------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * {
        margin: 0;
        padding: 0;
        font-family: 'Inter', sans-serif !important;
    }

    /* ---------- Dark page background ---------- */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }

    /* ---------- Main content ---------- */
    .main .block-container {
        padding-top: 2rem;
    }

    /* ---------- Title ---------- */
    h1 {
        background: linear-gradient(135deg, #00d2ff 0%, #7b2ff7 50%, #ff6fd8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    /* ---------- Subtitle ---------- */
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.55);
        font-size: 1.05rem;
        margin-bottom: 36px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* ---------- Section headers ---------- */
    h2 {
        background: linear-gradient(90deg, #00d2ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 1.6rem;
        margin-top: 42px;
        margin-bottom: 18px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(123,47,247,0.3);
    }

    h3 {
        color: rgba(255,255,255,0.85) !important;
        font-weight: 600;
        font-size: 1.25rem;
        margin-top: 28px;
        margin-bottom: 14px;
    }

    /* All text white on dark bg */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {
        color: rgba(255,255,255,0.85);
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        border-right: 1px solid rgba(123,47,247,0.2);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white !important;
    }

    /* ---------- Glassmorphism card (reusable) ---------- */
    .glass-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 26px;
        text-align: center;
        color: white;
        transition: all 0.4s cubic-bezier(.25,.8,.25,1);
        animation: fadeSlideUp 0.6s ease forwards;
        opacity: 0;
    }
    .glass-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 40px rgba(123,47,247,0.25);
        border-color: rgba(123,47,247,0.35);
    }

    /* Staggered animation delays */
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }

    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .card-label {
        font-size: 0.75rem;
        opacity: 0.7;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .card-value {
        font-size: 2.2rem;
        margin: 12px 0 6px;
        font-weight: 800;
    }
    .card-sub {
        font-size: 0.78rem;
        opacity: 0.5;
    }

    /* Neon accent borders on each card */
    .neon-purple  { border-top: 3px solid #7b2ff7; }
    .neon-cyan    { border-top: 3px solid #00d2ff; }
    .neon-pink    { border-top: 3px solid #ff6fd8; }
    .neon-green   { border-top: 3px solid #10B981; }
    .neon-orange  { border-top: 3px solid #f59e0b; }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #7b2ff7 0%, #00d2ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(123,47,247,0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(123,47,247,0.55) !important;
    }

    /* ---------- Radio / Tabs ---------- */
    .stRadio > div { gap: 0.5rem; }
    .stRadio label {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        transition: all 0.2s !important;
    }

    /* ---------- Expander ---------- */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* Fix expander icon overlap with label text */
    [data-testid="stExpander"] details {
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        background: rgba(255,255,255,0.04) !important;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        padding: 14px 18px !important;
        gap: 12px !important;
        display: flex !important;
        align-items: center !important;
    }
    [data-testid="stExpander"] summary span {
        overflow: visible !important;
        white-space: nowrap !important;
    }
    [data-testid="stExpander"] summary svg {
        flex-shrink: 0 !important;
        min-width: 16px !important;
        margin-right: 8px !important;
    }

    /* ---------- Slider ---------- */
    .stSlider [data-testid="stThumbValue"] {
        color: #00d2ff !important;
        font-weight: 700 !important;
    }

    /* ---------- Sidebar spacing fix ---------- */
    [data-testid="stSidebar"] .block-container,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        gap: 0.6rem !important;
    }
    [data-testid="stSidebar"] .stSlider {
        padding-bottom: 8px !important;
    }
    [data-testid="stSidebar"] hr {
        margin: 12px 0 !important;
    }

    /* ---------- Selectbox ---------- */
    .stSelectbox [data-baseweb="select"] {
        border-color: rgba(123,47,247,0.4) !important;
        background: rgba(255,255,255,0.06) !important;
    }

    /* ---------- DataFrame ---------- */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* ---------- Section spacing (prevent card bleed into next section) ---------- */
    .stColumns {
        margin-bottom: 24px !important;
    }
    h2 {
        margin-top: 52px !important;
    }

    /* ---------- Summary card ---------- */
    .summary-card {
        background: rgba(123,47,247,0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(123,47,247,0.2);
        border-radius: 16px;
        padding: 28px 32px;
        color: rgba(255,255,255,0.9);
        line-height: 1.7;
        font-size: 1rem;
        margin: 20px 0;
        animation: fadeSlideUp 0.6s ease forwards;
        opacity: 0;
        animation-delay: 0.5s;
    }

    /* ---------- Market indicator ---------- */
    .market-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 8px 0 16px;
    }
    .market-open {
        background: rgba(16,185,129,0.15);
        color: #10B981;
        border: 1px solid rgba(16,185,129,0.3);
    }
    .market-closed {
        background: rgba(239,68,68,0.15);
        color: #EF4444;
        border: 1px solid rgba(239,68,68,0.3);
    }
    .pulse-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
    .pulse-green { background: #10B981; }
    .pulse-red   { background: #EF4444; }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%      { opacity: 0.4; transform: scale(1.4); }
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        padding: 30px 20px 20px;
        color: rgba(255,255,255,0.35);
        font-size: 0.82rem;
        line-height: 1.6;
    }
    .footer-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #7b2ff7, #00d2ff, transparent);
        border: none;
        margin: 40px 0 24px;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# App Header
# ---------------------------------
st.markdown("<h1>🔮 StockVision</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>AI-Powered Stock Forecast • Real-Time Analytics • Prophet ML</p>",
    unsafe_allow_html=True
)

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# ---------------------------------
# Sidebar
# ---------------------------------
st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.markdown("---")

# Market status
now = datetime.now()
weekday = now.weekday()
hour = now.hour
market_open = weekday < 5 and 9 <= hour < 16  # approximate US market hours
if market_open:
    st.sidebar.markdown(
        '<div class="market-badge market-open"><span class="pulse-dot pulse-green"></span> Market Open</div>',
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        '<div class="market-badge market-closed"><span class="pulse-dot pulse-red"></span> Market Closed</div>',
        unsafe_allow_html=True
    )

stocks = ("GOOG", "AAPL", "MSFT", "AMZN", "TSLA", "META", "NFLX", "NVDA", "GME")
selected_stock = st.sidebar.selectbox("📊 Select Stock", stocks)

n_years = st.sidebar.slider("📅 Forecast Period", 1, 4, 2, help="Years to forecast")
period = n_years * 365

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Compare With")
compare_stock = st.sidebar.selectbox(
    "Overlay a second stock",
    ["None"] + [s for s in stocks if s != selected_stock],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Chart Type")
chart_type = st.sidebar.radio("Historical chart style", ["Line", "Candlestick"], horizontal=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "🚀 **StockVision** uses Facebook Prophet for time-series forecasting.\n\n"
    "**Data:** Yahoo Finance (daily updates)"
)

# ---------------------------------
# Data Loading
# ---------------------------------
@st.cache_data(ttl=3600)
def load_data(ticker):
    data = yf.download(ticker, START, TODAY, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.reset_index(inplace=True)
    return data

with st.spinner(f"📊 Loading {selected_stock} data..."):
    data = load_data(selected_stock)

compare_data = None
if compare_stock != "None":
    with st.spinner(f"📊 Loading {compare_stock} data..."):
        compare_data = load_data(compare_stock)

# ---------------------------------
# Helper: Dark Plotly layout
# ---------------------------------
PLOTLY_DARK = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="rgba(255,255,255,0.75)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
    legend=dict(
        bgcolor="rgba(0,0,0,0.3)",
        x=0.01, y=0.99,
        xanchor="left", yanchor="top",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
        font=dict(size=11),
    ),
    hoverlabel=dict(bgcolor="#1a1a2e", font_color="white", bordercolor="rgba(123,47,247,0.4)"),
    margin=dict(l=50, r=50, t=60, b=50),
)

# ---------------------------------
# Stock Overview Metrics
# ---------------------------------
st.markdown("<h2>📊 Stock Overview</h2>", unsafe_allow_html=True)

current_price = data["Close"].iloc[-1]
prev_price = data["Close"].iloc[-2] if len(data) > 1 else current_price
change = ((current_price - prev_price) / prev_price * 100) if prev_price != 0 else 0
high_price = data["Close"].max()
low_price = data["Close"].min()
avg_volume = data["Volume"].mean() if "Volume" in data.columns else 0

change_arrow = "▲" if change >= 0 else "▼"
change_color = "#10B981" if change >= 0 else "#EF4444"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card neon-purple delay-1">
        <div class="card-label">Current Price</div>
        <div class="card-value">${current_price:.2f}</div>
        <div class="card-sub">as of today</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card neon-pink delay-2">
        <div class="card-label">Day Change</div>
        <div class="card-value" style="color:{change_color}">{change_arrow} {change:+.2f}%</div>
        <div class="card-sub">24h performance</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card neon-cyan delay-3">
        <div class="card-label">All-Time High</div>
        <div class="card-value">${high_price:.2f}</div>
        <div class="card-sub">historical peak</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card neon-green delay-4">
        <div class="card-label">Avg Volume</div>
        <div class="card-value">{avg_volume/1e6:.1f}M</div>
        <div class="card-sub">shares / day</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# Raw Data Expander
# ---------------------------------
with st.expander("📋 View Raw Historical Data", expanded=False):
    st.dataframe(data.tail(20), use_container_width=True, hide_index=True)

# ---------------------------------
# Historical Price Chart
# ---------------------------------
st.markdown("<h2>📈 Historical Price Trends</h2>", unsafe_allow_html=True)

if chart_type == "Candlestick":
    fig_hist = go.Figure(data=[go.Candlestick(
        x=data["Date"],
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        increasing_line_color="#10B981",
        decreasing_line_color="#EF4444",
        name=selected_stock
    )])
else:
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=data["Date"], y=data["Open"],
        name="Open",
        line=dict(color="#00d2ff", width=2),
        hovertemplate='<b>Open</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>'
    ))
    fig_hist.add_trace(go.Scatter(
        x=data["Date"], y=data["Close"],
        name="Close",
        line=dict(color="#ff6fd8", width=2),
        fill='tonexty',
        fillcolor='rgba(123,47,247,0.08)',
        hovertemplate='<b>Close</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>'
    ))

# Comparison overlay
if compare_data is not None:
    fig_hist.add_trace(go.Scatter(
        x=compare_data["Date"], y=compare_data["Close"],
        name=f"{compare_stock} Close",
        line=dict(color="#f59e0b", width=2, dash="dot"),
        yaxis="y2",
        hovertemplate=f'<b>{compare_stock}</b><br>%{{x|%Y-%m-%d}}<br>${{y:.2f}}<extra></extra>'
    ))
    fig_hist.update_layout(
        yaxis2=dict(
            title=f"{compare_stock} Price (USD)",
            overlaying="y", side="right",
            gridcolor="rgba(255,255,255,0.04)",
            color="rgba(255,255,255,0.5)"
        )
    )

fig_hist.update_layout(
    title=f"{selected_stock} — Historical Data" + (f" vs {compare_stock}" if compare_data is not None else ""),
    xaxis_title="Date", yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
    hovermode='x unified',
    height=520,
    **PLOTLY_DARK
)
st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------------
# Volume Analysis
# ---------------------------------
st.markdown("<h2>📊 Volume Analysis</h2>", unsafe_allow_html=True)

if "Volume" in data.columns:
    vol_data = data.copy()
    vol_data["Vol_MA20"] = vol_data["Volume"].rolling(20).mean()

    fig_vol = go.Figure()
    colors = ["#10B981" if c >= o else "#EF4444"
              for c, o in zip(vol_data["Close"], vol_data["Open"])]
    fig_vol.add_trace(go.Bar(
        x=vol_data["Date"], y=vol_data["Volume"],
        name="Volume",
        marker_color=colors,
        opacity=0.5,
        hovertemplate='<b>Volume</b><br>%{x|%Y-%m-%d}<br>%{y:,.0f}<extra></extra>'
    ))
    fig_vol.add_trace(go.Scatter(
        x=vol_data["Date"], y=vol_data["Vol_MA20"],
        name="20-Day MA",
        line=dict(color="#f59e0b", width=2),
        hovertemplate='<b>20-Day MA</b><br>%{y:,.0f}<extra></extra>'
    ))
    fig_vol.update_layout(
        title=f"{selected_stock} — Daily Volume",
        xaxis_title="Date", yaxis_title="Volume",
        height=380, barmode="overlay",
        **PLOTLY_DARK
    )
    st.plotly_chart(fig_vol, use_container_width=True)

# ---------------------------------
# Technical Indicators (MAs)
# ---------------------------------
st.markdown("<h2>🔬 Technical Indicators</h2>", unsafe_allow_html=True)

ma_data = data.copy()
ma_data["MA50"] = ma_data["Close"].rolling(50).mean()
ma_data["MA200"] = ma_data["Close"].rolling(200).mean()

fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(
    x=ma_data["Date"], y=ma_data["Close"],
    name="Close Price",
    line=dict(color="#ff6fd8", width=2),
))
fig_ma.add_trace(go.Scatter(
    x=ma_data["Date"], y=ma_data["MA50"],
    name="50-Day MA",
    line=dict(color="#00d2ff", width=2, dash="dash"),
))
fig_ma.add_trace(go.Scatter(
    x=ma_data["Date"], y=ma_data["MA200"],
    name="200-Day MA",
    line=dict(color="#f59e0b", width=2, dash="dot"),
))
fig_ma.update_layout(
    title=f"{selected_stock} — Moving Averages (50 & 200 Day)",
    xaxis_title="Date", yaxis_title="Price (USD)",
    height=460, hovermode='x unified',
    **PLOTLY_DARK
)
st.plotly_chart(fig_ma, use_container_width=True)

# MA signal
latest_ma50 = ma_data["MA50"].dropna().iloc[-1] if ma_data["MA50"].dropna().shape[0] > 0 else None
latest_ma200 = ma_data["MA200"].dropna().iloc[-1] if ma_data["MA200"].dropna().shape[0] > 0 else None
if latest_ma50 is not None and latest_ma200 is not None:
    if latest_ma50 > latest_ma200:
        st.markdown(
            '<div class="summary-card">📈 <strong>Golden Cross Signal:</strong> '
            'The 50-day MA is <em>above</em> the 200-day MA, suggesting a <span style="color:#10B981;font-weight:700">bullish</span> trend.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="summary-card">📉 <strong>Death Cross Signal:</strong> '
            'The 50-day MA is <em>below</em> the 200-day MA, suggesting a <span style="color:#EF4444;font-weight:700">bearish</span> trend.</div>',
            unsafe_allow_html=True
        )

# ---------------------------------
# Prophet Forecast
# ---------------------------------
df_train = data[["Date", "Close"]].copy()
df_train.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)
df_train["ds"] = pd.to_datetime(df_train["ds"])
df_train["y"] = pd.to_numeric(df_train["y"])

@st.cache_resource
def train_model(df):
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df[["ds", "y"]])
    return model

with st.spinner("🤖 Training forecasting model..."):
    model = train_model(df_train)
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)

# ---------------------------------
# Forecast Metrics
# ---------------------------------
st.markdown(f"<h2>🔮 {n_years}-Year Forecast Analysis</h2>", unsafe_allow_html=True)

forecast_latest = forecast["yhat"].iloc[-1]
forecast_mean = forecast["yhat"].mean()
forecast_high = forecast["yhat_upper"].max()
forecast_low = forecast["yhat_lower"].min()
price_growth = ((forecast_latest - current_price) / current_price * 100) if current_price != 0 else 0
growth_arrow = "▲" if price_growth >= 0 else "▼"
growth_color = "#10B981" if price_growth >= 0 else "#EF4444"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card neon-purple delay-1">
        <div class="card-label">Predicted Price</div>
        <div class="card-value">${forecast_latest:.2f}</div>
        <div class="card-sub">end of forecast</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card neon-cyan delay-2">
        <div class="card-label">Avg Forecast</div>
        <div class="card-value">${forecast_mean:.2f}</div>
        <div class="card-sub">mean prediction</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card neon-orange delay-3">
        <div class="card-label">Upper Band (95%)</div>
        <div class="card-value">${forecast_high:.2f}</div>
        <div class="card-sub">confidence ceiling</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card neon-pink delay-4">
        <div class="card-label">Growth Forecast</div>
        <div class="card-value" style="color:{growth_color}">{growth_arrow} {price_growth:+.1f}%</div>
        <div class="card-sub">vs current price</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# Forecast Summary Card
# ---------------------------------
trend_word = "upward" if price_growth >= 0 else "downward"
trend_emoji = "📈" if price_growth >= 0 else "📉"
st.markdown(f"""
<div class="summary-card">
    {trend_emoji} <strong>Forecast Summary:</strong>
    Based on Prophet's analysis of <strong>{selected_stock}</strong>,
    the model projects an <strong>{trend_word}</strong> trajectory over the next <strong>{n_years} year(s)</strong>.
    The predicted price at the end of the forecast window is <strong>${forecast_latest:.2f}</strong>
    (a <span style="color:{growth_color};font-weight:700">{price_growth:+.1f}%</span> change from the current ${current_price:.2f}).
    The 95% confidence band ranges from <strong>${forecast_low:.2f}</strong> to <strong>${forecast_high:.2f}</strong>.
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# Forecast Chart
# ---------------------------------
st.markdown("<h3>📊 Forecast Visualization</h3>", unsafe_allow_html=True)

fig_forecast = plot_plotly(model, forecast)
fig_forecast.update_layout(
    title=f"{selected_stock} — Price Forecast ({n_years} Year{'s' if n_years > 1 else ''})",
    height=520,
    **PLOTLY_DARK
)
fig_forecast.update_xaxes(title_text="Date")
fig_forecast.update_yaxes(title_text="Price (USD)")
st.plotly_chart(fig_forecast, use_container_width=True)

# ---------------------------------
# Forecast Components
# ---------------------------------
st.markdown("<h3>🔍 Forecast Components (Seasonality & Trend)</h3>", unsafe_allow_html=True)

with st.expander("📊 View Detailed Components", expanded=False):
    fig_components = model.plot_components(forecast)
    st.pyplot(fig_components, use_container_width=True)

# ---------------------------------
# Forecast Table
# ---------------------------------
with st.expander("📋 View Detailed Forecast Data", expanded=False):
    forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).copy()
    forecast_display.columns = ['Date', 'Forecast Price', 'Lower Bound', 'Upper Bound']
    forecast_display['Date'] = forecast_display['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(forecast_display, use_container_width=True, hide_index=True)

# ---------------------------------
# Footer
# ---------------------------------
st.markdown('<div class="footer-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div style="font-size:1.2rem; margin-bottom:6px;">🔮 StockVision</div>
    <div>Built with Streamlit • Prophet ML • Yahoo Finance</div>
    <div style="margin-top:10px; opacity:0.6;">
        ⚠️ This tool is for educational purposes only. Not financial advice. Always consult a professional advisor.
    </div>
</div>
""", unsafe_allow_html=True)
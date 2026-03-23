import React from 'react';
import { FiTrendingUp, FiSettings, FiBarChart2 } from 'react-icons/fi';

const STOCKS = ['GOOG', 'AAPL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'GME'];

export default function Sidebar({
  selectedStock,
  setSelectedStock,
  years,
  setYears,
  chartType,
  setChartType,
  compareStock,
  setCompareStock,
  marketStatus,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-icon">🔮</span>
          <span className="logo-text">StockVision</span>
        </div>
        <p className="sidebar-tagline">AI-Powered Analytics</p>
      </div>

      <div className="sidebar-divider" />

      {/* Market Status */}
      <div className={`market-badge ${marketStatus?.is_open ? 'market-open' : 'market-closed'}`}>
        <span className={`pulse-dot ${marketStatus?.is_open ? 'pulse-green' : 'pulse-red'}`} />
        {marketStatus?.is_open ? 'Market Open' : 'Market Closed'}
      </div>

      <div className="sidebar-divider" />

      {/* Stock Selector */}
      <div className="sidebar-section">
        <label className="sidebar-label">
          <FiBarChart2 /> Select Stock
        </label>
        <select
          id="stock-selector"
          className="sidebar-select"
          value={selectedStock}
          onChange={e => setSelectedStock(e.target.value)}
        >
          {STOCKS.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Forecast Slider */}
      <div className="sidebar-section">
        <label className="sidebar-label">
          <FiTrendingUp /> Forecast: {years} Year{years > 1 ? 's' : ''}
        </label>
        <input
          id="forecast-slider"
          type="range"
          min={1}
          max={4}
          value={years}
          onChange={e => setYears(Number(e.target.value))}
          className="sidebar-slider"
        />
        <div className="slider-labels">
          <span>1Y</span><span>2Y</span><span>3Y</span><span>4Y</span>
        </div>
      </div>

      <div className="sidebar-divider" />

      {/* Chart Type */}
      <div className="sidebar-section">
        <label className="sidebar-label">
          <FiSettings /> Chart Type
        </label>
        <div className="toggle-group">
          <button
            className={`toggle-btn ${chartType === 'Line' ? 'active' : ''}`}
            onClick={() => setChartType('Line')}
          >
            Line
          </button>
          <button
            className={`toggle-btn ${chartType === 'Candlestick' ? 'active' : ''}`}
            onClick={() => setChartType('Candlestick')}
          >
            Candle
          </button>
        </div>
      </div>

      <div className="sidebar-divider" />

      {/* Comparison */}
      <div className="sidebar-section">
        <label className="sidebar-label">
          <FiBarChart2 /> Compare With
        </label>
        <select
          id="compare-selector"
          className="sidebar-select"
          value={compareStock}
          onChange={e => setCompareStock(e.target.value)}
        >
          <option value="None">None</option>
          {STOCKS.filter(s => s !== selectedStock).map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      <div className="sidebar-divider" />

      <div className="sidebar-info">
        <p>🚀 <strong>StockVision</strong> uses Facebook Prophet for time-series forecasting.</p>
        <p className="info-sub">Data: Yahoo Finance (daily updates)</p>
      </div>
    </aside>
  );
}

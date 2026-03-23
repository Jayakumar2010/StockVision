import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import MetricCards from './components/MetricCards';
import HistoricalChart from './components/HistoricalChart';
import VolumeChart from './components/VolumeChart';
import TechnicalIndicators from './components/TechnicalIndicators';
import ForecastSummary from './components/ForecastSummary';
import ForecastChart from './components/ForecastChart';
import DataTable from './components/DataTable';
import Footer from './components/Footer';
import { useStockData, useForecast, useMarketStatus } from './hooks/useStockData';

function LoadingSpinner({ text }) {
  return (
    <div className="loading-container">
      <div className="spinner" />
      <p className="loading-text">{text}</p>
    </div>
  );
}

function ErrorBanner({ message, onRetry }) {
  return (
    <div className="error-banner">
      <p>⚠️ {message}</p>
      {onRetry && <button className="retry-btn" onClick={onRetry}>Retry</button>}
    </div>
  );
}

const RAW_COLUMNS = [
  { key: 'Date', label: 'Date' },
  { key: 'Open', label: 'Open', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
  { key: 'High', label: 'High', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
  { key: 'Low', label: 'Low', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
  { key: 'Close', label: 'Close', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
  { key: 'Volume', label: 'Volume', format: v => v != null ? Number(v).toLocaleString() : '—' },
];

const FORECAST_COLUMNS = [
  { key: 'ds', label: 'Date' },
  { key: 'yhat', label: 'Forecast', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
  { key: 'yhat_lower', label: 'Lower Bound', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
  { key: 'yhat_upper', label: 'Upper Bound', format: v => v != null ? `$${Number(v).toFixed(2)}` : '—' },
];

export default function App() {
  const [selectedStock, setSelectedStock] = useState('GOOG');
  const [years, setYears] = useState(2);
  const [chartType, setChartType] = useState('Line');
  const [compareStock, setCompareStock] = useState('None');

  const marketStatus = useMarketStatus();
  const { stockData, summary, loading: stockLoading, error: stockError, refetch: refetchStock } = useStockData(selectedStock);
  const { stockData: compareData } = useStockData(compareStock === 'None' ? null : compareStock);
  const { forecast, forecastSummary, loading: forecastLoading, error: forecastError, refetch: refetchForecast } = useForecast(selectedStock, years);

  return (
    <div className="app-layout">
      <Sidebar
        selectedStock={selectedStock}
        setSelectedStock={setSelectedStock}
        years={years}
        setYears={setYears}
        chartType={chartType}
        setChartType={setChartType}
        compareStock={compareStock}
        setCompareStock={setCompareStock}
        marketStatus={marketStatus}
      />

      <main className="main-content">
        {/* Header */}
        <header className="app-header">
          <h1>🔮 StockVision</h1>
          <p className="subtitle">AI-Powered Stock Forecast • Real-Time Analytics • Prophet ML</p>
        </header>

        {/* Stock Overview */}
        {stockLoading && <LoadingSpinner text={`Loading ${selectedStock} data...`} />}
        {stockError && <ErrorBanner message={stockError} onRetry={refetchStock} />}

        {!stockLoading && !stockError && stockData && (
          <>
            <section className="chart-section">
              <h2>📊 Stock Overview</h2>
              <MetricCards summary={summary} ticker={selectedStock} />
            </section>

            <DataTable
              title="📋 View Raw Historical Data"
              data={stockData}
              columns={RAW_COLUMNS}
              maxRows={30}
            />

            <HistoricalChart
              data={stockData}
              chartType={chartType}
              ticker={selectedStock}
              compareData={compareData}
              compareStock={compareStock}
            />

            <VolumeChart data={stockData} ticker={selectedStock} />

            <TechnicalIndicators
              data={stockData}
              ticker={selectedStock}
              summary={summary}
            />
          </>
        )}

        {/* Forecast Section */}
        {forecastLoading && <LoadingSpinner text="🤖 Training forecasting model..." />}
        {forecastError && <ErrorBanner message={forecastError} onRetry={refetchForecast} />}

        {!forecastLoading && !forecastError && forecast && (
          <>
            <ForecastSummary
              forecastSummary={forecastSummary}
              ticker={selectedStock}
              years={years}
            />

            <section className="chart-section">
              <h2>📊 Forecast Visualization</h2>
              <ForecastChart
                forecast={forecast}
                ticker={selectedStock}
                years={years}
              />
            </section>

            <DataTable
              title="📋 View Detailed Forecast Data"
              data={forecast}
              columns={FORECAST_COLUMNS}
              maxRows={30}
            />
          </>
        )}

        <Footer />
      </main>
    </div>
  );
}

import { useState, useEffect, useCallback } from 'react';

const API_BASE = '/api';

export function useStockData(ticker) {
  const [stockData, setStockData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStock = useCallback(async () => {
    if (!ticker) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/stock/${ticker}`);
      if (!res.ok) throw new Error(`Failed to fetch ${ticker} data`);
      const json = await res.json();
      setStockData(json.data);
      setSummary(json.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [ticker]);

  useEffect(() => {
    fetchStock();
  }, [fetchStock]);

  return { stockData, summary, loading, error, refetch: fetchStock };
}

export function useForecast(ticker, years) {
  const [forecast, setForecast] = useState(null);
  const [forecastSummary, setForecastSummary] = useState(null);
  const [components, setComponents] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchForecast = useCallback(async () => {
    if (!ticker) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/forecast/${ticker}?years=${years}`);
      if (!res.ok) throw new Error(`Failed to fetch forecast for ${ticker}`);
      const json = await res.json();
      setForecast(json.forecast);
      setForecastSummary(json.summary);
      setComponents(json.components);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [ticker, years]);

  useEffect(() => {
    fetchForecast();
  }, [fetchForecast]);

  return { forecast, forecastSummary, components, loading, error, refetch: fetchForecast };
}

export function useMarketStatus() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/market-status`)
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(() => setStatus({ is_open: false }));
  }, []);

  return status;
}

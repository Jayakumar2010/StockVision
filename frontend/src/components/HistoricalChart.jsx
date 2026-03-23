import React, { useEffect, useRef } from 'react';
import {
  ResponsiveContainer, ComposedChart, Line, Area, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend,
} from 'recharts';
import { createChart, CandlestickSeries } from 'lightweight-charts';

const CHART_COLORS = {
  open: '#00d2ff',
  close: '#ff6fd8',
  compare: '#f59e0b',
  area: 'rgba(123,47,247,0.08)',
  grid: 'rgba(255,255,255,0.06)',
};

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip">
      <p className="tooltip-date">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: ${Number(p.value).toFixed(2)}
        </p>
      ))}
    </div>
  );
}

function LineChart({ data, compareData, compareStock, ticker }) {
  // sample data for performance (show every Nth point)
  const sampleRate = Math.max(1, Math.floor(data.length / 500));
  const sampled = data.filter((_, i) => i % sampleRate === 0 || i === data.length - 1);

  return (
    <ResponsiveContainer width="100%" height={480}>
      <ComposedChart data={sampled} margin={{ top: 10, right: 60, left: 10, bottom: 10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.grid} />
        <XAxis
          dataKey="Date"
          stroke="rgba(255,255,255,0.4)"
          tick={{ fontSize: 11 }}
          tickFormatter={d => d?.slice(0, 7)}
          interval={Math.floor(sampled.length / 8)}
        />
        <YAxis stroke="rgba(255,255,255,0.4)" tick={{ fontSize: 11 }} domain={['auto', 'auto']} />
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ color: 'rgba(255,255,255,0.7)', fontSize: 12 }} />
        <Area
          type="monotone"
          dataKey="Close"
          stroke={CHART_COLORS.close}
          fill={CHART_COLORS.area}
          strokeWidth={2}
          name={`${ticker} Close`}
          dot={false}
        />
        <Line
          type="monotone"
          dataKey="Open"
          stroke={CHART_COLORS.open}
          strokeWidth={1.5}
          name={`${ticker} Open`}
          dot={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}

function CandlestickChart({ data, ticker }) {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartContainerRef.current || !data?.length) return;

    // Clean up previous chart
    if (chartRef.current) {
      chartRef.current.remove();
      chartRef.current = null;
    }

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 480,
      layout: {
        background: { color: 'transparent' },
        textColor: 'rgba(255,255,255,0.6)',
        fontFamily: 'Inter, sans-serif',
      },
      grid: {
        vertLines: { color: 'rgba(255,255,255,0.04)' },
        horzLines: { color: 'rgba(255,255,255,0.04)' },
      },
      crosshair: { mode: 0 },
      timeScale: {
        borderColor: 'rgba(255,255,255,0.1)',
        timeVisible: false,
      },
      rightPriceScale: {
        borderColor: 'rgba(255,255,255,0.1)',
      },
    });

    const series = chart.addSeries(CandlestickSeries, {
      upColor: '#10B981',
      downColor: '#EF4444',
      borderUpColor: '#10B981',
      borderDownColor: '#EF4444',
      wickUpColor: '#10B981',
      wickDownColor: '#EF4444',
    });

    const candleData = data
      .filter(d => d.Date && d.Open != null && d.High != null && d.Low != null && d.Close != null)
      .map(d => ({
        time: d.Date,
        open: Number(d.Open),
        high: Number(d.High),
        low: Number(d.Low),
        close: Number(d.Close),
      }));

    series.setData(candleData);
    chart.timeScale().fitContent();
    chartRef.current = chart;

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [data]);

  return <div ref={chartContainerRef} className="candlestick-container" />;
}

export default function HistoricalChart({ data, chartType, ticker, compareData, compareStock }) {
  if (!data?.length) return null;

  return (
    <section className="chart-section">
      <h2>📈 Historical Price Trends</h2>
      <div className="chart-card">
        <div className="chart-card-header">
          <span>{ticker} — Historical Data</span>
          {compareStock !== 'None' && <span className="compare-badge">vs {compareStock}</span>}
        </div>
        {chartType === 'Candlestick' ? (
          <CandlestickChart data={data} ticker={ticker} />
        ) : (
          <LineChart data={data} compareData={compareData} compareStock={compareStock} ticker={ticker} />
        )}
      </div>
    </section>
  );
}

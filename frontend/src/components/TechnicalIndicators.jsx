import React from 'react';
import {
  ResponsiveContainer, ComposedChart, Line, Area, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ReferenceLine,
} from 'recharts';

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip">
      <p className="tooltip-date">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: {p.name === 'RSI' ? Number(p.value).toFixed(1) : `$${Number(p.value).toFixed(2)}`}
        </p>
      ))}
    </div>
  );
}

export default function TechnicalIndicators({ data, ticker, summary }) {
  if (!data?.length) return null;

  const sampleRate = Math.max(1, Math.floor(data.length / 500));
  const sampled = data.filter((_, i) => i % sampleRate === 0 || i === data.length - 1);

  // RSI data (last 200 points)
  const rsiData = data.slice(-200).filter(d => d.RSI != null);

  return (
    <section className="chart-section">
      <h2>🔬 Technical Indicators</h2>

      {/* MA Chart */}
      <div className="chart-card">
        <div className="chart-card-header">
          <span>{ticker} — Moving Averages (50 & 200 Day)</span>
        </div>
        <ResponsiveContainer width="100%" height={440}>
          <ComposedChart data={sampled} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
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
            <Line type="monotone" dataKey="Close" name="Close Price" stroke="#ff6fd8" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="MA50" name="50-Day MA" stroke="#00d2ff" strokeWidth={2} strokeDasharray="6 3" dot={false} />
            <Line type="monotone" dataKey="MA200" name="200-Day MA" stroke="#f59e0b" strokeWidth={2} strokeDasharray="3 3" dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* MA Signal */}
      {summary?.ma_signal && (
        <div className="summary-card">
          {summary.ma_signal === 'golden_cross' ? (
            <>📈 <strong>Golden Cross Signal:</strong> The 50-day MA is <em>above</em> the 200-day MA, suggesting a <span className="text-green">bullish</span> trend.</>
          ) : (
            <>📉 <strong>Death Cross Signal:</strong> The 50-day MA is <em>below</em> the 200-day MA, suggesting a <span className="text-red">bearish</span> trend.</>
          )}
        </div>
      )}

      {/* RSI Chart */}
      {rsiData.length > 0 && (
        <div className="chart-card" style={{ marginTop: 24 }}>
          <div className="chart-card-header">
            <span>{ticker} — RSI (14-Period)</span>
            {summary?.latest_rsi && (
              <span className={`rsi-badge ${summary.latest_rsi > 70 ? 'rsi-overbought' : summary.latest_rsi < 30 ? 'rsi-oversold' : 'rsi-neutral'}`}>
                RSI: {summary.latest_rsi.toFixed(1)}
              </span>
            )}
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <ComposedChart data={rsiData} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis
                dataKey="Date"
                stroke="rgba(255,255,255,0.4)"
                tick={{ fontSize: 11 }}
                tickFormatter={d => d?.slice(5)}
                interval={Math.floor(rsiData.length / 8)}
              />
              <YAxis stroke="rgba(255,255,255,0.4)" tick={{ fontSize: 11 }} domain={[0, 100]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={70} stroke="#EF4444" strokeDasharray="4 4" label={{ value: 'Overbought', fill: '#EF4444', fontSize: 11 }} />
              <ReferenceLine y={30} stroke="#10B981" strokeDasharray="4 4" label={{ value: 'Oversold', fill: '#10B981', fontSize: 11 }} />
              <Area type="monotone" dataKey="RSI" name="RSI" stroke="#7b2ff7" fill="rgba(123,47,247,0.15)" strokeWidth={2} dot={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Bollinger Bands */}
      <div className="chart-card" style={{ marginTop: 24 }}>
        <div className="chart-card-header">
          <span>{ticker} — Bollinger Bands (20-Period)</span>
        </div>
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart data={sampled} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
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
            <Area type="monotone" dataKey="BB_Upper" name="Upper Band" stroke="rgba(0,210,255,0.4)" fill="rgba(0,210,255,0.05)" dot={false} />
            <Area type="monotone" dataKey="BB_Lower" name="Lower Band" stroke="rgba(0,210,255,0.4)" fill="rgba(0,210,255,0.05)" dot={false} />
            <Line type="monotone" dataKey="BB_Mid" name="Middle Band" stroke="#00d2ff" strokeWidth={1} strokeDasharray="4 4" dot={false} />
            <Line type="monotone" dataKey="Close" name="Close" stroke="#ff6fd8" strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* MACD Chart */}
      <div className="chart-card" style={{ marginTop: 24 }}>
        <div className="chart-card-header">
          <span>{ticker} — MACD</span>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={sampled} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis
              dataKey="Date"
              stroke="rgba(255,255,255,0.4)"
              tick={{ fontSize: 11 }}
              tickFormatter={d => d?.slice(0, 7)}
              interval={Math.floor(sampled.length / 8)}
            />
            <YAxis stroke="rgba(255,255,255,0.4)" tick={{ fontSize: 11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ color: 'rgba(255,255,255,0.7)', fontSize: 12 }} />
            <Line type="monotone" dataKey="MACD" name="MACD" stroke="#00d2ff" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="MACD_Signal" name="Signal" stroke="#ff6fd8" strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

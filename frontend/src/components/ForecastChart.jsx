import React from 'react';
import {
  ResponsiveContainer, ComposedChart, Line, Area, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend,
} from 'recharts';

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

export default function ForecastChart({ forecast, ticker, years }) {
  if (!forecast?.length) return null;

  // Sample for performance
  const sampleRate = Math.max(1, Math.floor(forecast.length / 600));
  const sampled = forecast
    .filter((_, i) => i % sampleRate === 0 || i === forecast.length - 1)
    .map(d => ({
      date: d.ds,
      yhat: d.yhat ? Number(d.yhat).toFixed(2) : null,
      yhat_upper: d.yhat_upper ? Number(d.yhat_upper).toFixed(2) : null,
      yhat_lower: d.yhat_lower ? Number(d.yhat_lower).toFixed(2) : null,
    }));

  return (
    <div className="chart-card">
      <div className="chart-card-header">
        <span>{ticker} — Price Forecast ({years} Year{years > 1 ? 's' : ''})</span>
      </div>
      <ResponsiveContainer width="100%" height={480}>
        <ComposedChart data={sampled} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis
            dataKey="date"
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
            dataKey="yhat_upper"
            name="Upper Bound (95%)"
            stroke="rgba(0,210,255,0.3)"
            fill="rgba(0,210,255,0.08)"
            dot={false}
          />
          <Area
            type="monotone"
            dataKey="yhat_lower"
            name="Lower Bound (95%)"
            stroke="rgba(0,210,255,0.3)"
            fill="rgba(15,12,41,0.9)"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="yhat"
            name="Predicted Price"
            stroke="#7b2ff7"
            strokeWidth={2.5}
            dot={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

import React from 'react';
import {
  ResponsiveContainer, ComposedChart, Bar, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend,
} from 'recharts';

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip">
      <p className="tooltip-date">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: {Number(p.value).toLocaleString()}
        </p>
      ))}
    </div>
  );
}

export default function VolumeChart({ data, ticker }) {
  if (!data?.length) return null;

  // Sample for performance
  const sampleRate = Math.max(1, Math.floor(data.length / 400));
  const sampled = data
    .filter((_, i) => i % sampleRate === 0 || i === data.length - 1)
    .map(d => ({
      ...d,
      fillColor: (d.Close >= d.Open) ? 'rgba(16,185,129,0.5)' : 'rgba(239,68,68,0.5)',
    }));

  return (
    <section className="chart-section">
      <h2>📊 Volume Analysis</h2>
      <div className="chart-card">
        <div className="chart-card-header">
          <span>{ticker} — Daily Volume</span>
        </div>
        <ResponsiveContainer width="100%" height={360}>
          <ComposedChart data={sampled} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis
              dataKey="Date"
              stroke="rgba(255,255,255,0.4)"
              tick={{ fontSize: 11 }}
              tickFormatter={d => d?.slice(0, 7)}
              interval={Math.floor(sampled.length / 8)}
            />
            <YAxis
              stroke="rgba(255,255,255,0.4)"
              tick={{ fontSize: 11 }}
              tickFormatter={v => v >= 1e6 ? `${(v / 1e6).toFixed(0)}M` : v.toLocaleString()}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ color: 'rgba(255,255,255,0.7)', fontSize: 12 }} />
            <Bar
              dataKey="Volume"
              name="Volume"
              fill="rgba(123,47,247,0.4)"
              radius={[2, 2, 0, 0]}
            />
            <Line
              type="monotone"
              dataKey="Vol_MA20"
              name="20-Day MA"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

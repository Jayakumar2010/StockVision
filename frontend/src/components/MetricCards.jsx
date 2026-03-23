import React from 'react';
import { FiTrendingUp, FiTrendingDown, FiDollarSign, FiBarChart2 } from 'react-icons/fi';

function formatVolume(v) {
  if (!v) return '0';
  if (v >= 1e9) return (v / 1e9).toFixed(1) + 'B';
  if (v >= 1e6) return (v / 1e6).toFixed(1) + 'M';
  if (v >= 1e3) return (v / 1e3).toFixed(1) + 'K';
  return v.toFixed(0);
}

export default function MetricCards({ summary, ticker }) {
  if (!summary) return null;

  const { current_price, change_pct, high_price, avg_volume } = summary;
  const isUp = change_pct >= 0;

  const cards = [
    {
      label: 'Current Price',
      value: `$${current_price.toFixed(2)}`,
      sub: 'as of today',
      accent: 'neon-purple',
      icon: <FiDollarSign />,
    },
    {
      label: 'Day Change',
      value: `${isUp ? '▲' : '▼'} ${change_pct >= 0 ? '+' : ''}${change_pct.toFixed(2)}%`,
      sub: '24h performance',
      accent: 'neon-pink',
      valueColor: isUp ? '#10B981' : '#EF4444',
      icon: isUp ? <FiTrendingUp /> : <FiTrendingDown />,
    },
    {
      label: 'All-Time High',
      value: `$${high_price.toFixed(2)}`,
      sub: 'historical peak',
      accent: 'neon-cyan',
      icon: <FiTrendingUp />,
    },
    {
      label: 'Avg Volume',
      value: formatVolume(avg_volume),
      sub: 'shares / day',
      accent: 'neon-green',
      icon: <FiBarChart2 />,
    },
  ];

  return (
    <div className="metric-grid">
      {cards.map((card, i) => (
        <div key={card.label} className={`glass-card ${card.accent} delay-${i + 1}`}>
          <div className="card-icon">{card.icon}</div>
          <div className="card-label">{card.label}</div>
          <div className="card-value" style={card.valueColor ? { color: card.valueColor } : {}}>
            {card.value}
          </div>
          <div className="card-sub">{card.sub}</div>
        </div>
      ))}
    </div>
  );
}

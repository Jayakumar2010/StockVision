import React from 'react';
import { FiTrendingUp, FiTrendingDown, FiTarget, FiActivity } from 'react-icons/fi';

export default function ForecastSummary({ forecastSummary, ticker, years }) {
  if (!forecastSummary) return null;

  const {
    current_price, predicted_price, mean_forecast,
    upper_band, lower_band, growth_pct
  } = forecastSummary;

  const isUp = growth_pct >= 0;
  const growthColor = isUp ? '#10B981' : '#EF4444';

  const cards = [
    {
      label: 'Predicted Price',
      value: `$${predicted_price.toFixed(2)}`,
      sub: 'end of forecast',
      accent: 'neon-purple',
      icon: <FiTarget />,
    },
    {
      label: 'Avg Forecast',
      value: `$${mean_forecast.toFixed(2)}`,
      sub: 'mean prediction',
      accent: 'neon-cyan',
      icon: <FiActivity />,
    },
    {
      label: 'Upper Band (95%)',
      value: `$${upper_band.toFixed(2)}`,
      sub: 'confidence ceiling',
      accent: 'neon-orange',
      icon: <FiTrendingUp />,
    },
    {
      label: 'Growth Forecast',
      value: `${isUp ? '▲' : '▼'} ${growth_pct >= 0 ? '+' : ''}${growth_pct.toFixed(1)}%`,
      sub: 'vs current price',
      accent: 'neon-pink',
      valueColor: growthColor,
      icon: isUp ? <FiTrendingUp /> : <FiTrendingDown />,
    },
  ];

  const trendWord = isUp ? 'upward' : 'downward';
  const trendEmoji = isUp ? '📈' : '📉';

  return (
    <section className="chart-section">
      <h2>🔮 {years}-Year Forecast Analysis</h2>

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

      <div className="summary-card">
        {trendEmoji} <strong>Forecast Summary:</strong> Based on Prophet's analysis of <strong>{ticker}</strong>,
        the model projects an <strong>{trendWord}</strong> trajectory over the next <strong>{years} year{years > 1 ? 's' : ''}</strong>.
        The predicted price at the end of the forecast window is <strong>${predicted_price.toFixed(2)}</strong>
        {' '}(a <span style={{ color: growthColor, fontWeight: 700 }}>{growth_pct >= 0 ? '+' : ''}{growth_pct.toFixed(1)}%</span> change from the current ${current_price.toFixed(2)}).
        The 95% confidence band ranges from <strong>${lower_band.toFixed(2)}</strong> to <strong>${upper_band.toFixed(2)}</strong>.
      </div>
    </section>
  );
}

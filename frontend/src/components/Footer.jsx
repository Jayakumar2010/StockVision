import React from 'react';

export default function Footer() {
  return (
    <>
      <div className="footer-divider" />
      <footer className="footer">
        <div className="footer-logo">🔮 StockVision</div>
        <div>Built with React • Prophet ML • Yahoo Finance</div>
        <div className="footer-disclaimer">
          ⚠️ This tool is for educational purposes only. Not financial advice. Always consult a professional advisor.
        </div>
      </footer>
    </>
  );
}

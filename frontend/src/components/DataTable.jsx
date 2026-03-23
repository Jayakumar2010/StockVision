import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';

export default function DataTable({ title, data, columns, maxRows = 20 }) {
  const [expanded, setExpanded] = useState(false);
  if (!data?.length) return null;

  const displayData = expanded ? data.slice(-maxRows) : [];

  return (
    <div className="data-table-wrapper">
      <button
        className="expander-btn"
        onClick={() => setExpanded(!expanded)}
        id={`table-${title.replace(/\s+/g, '-').toLowerCase()}`}
      >
        <span>{title}</span>
        {expanded ? <FiChevronUp /> : <FiChevronDown />}
      </button>

      {expanded && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                {columns.map(col => (
                  <th key={col.key}>{col.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {displayData.map((row, i) => (
                <tr key={i}>
                  {columns.map(col => (
                    <td key={col.key}>
                      {col.format ? col.format(row[col.key]) : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

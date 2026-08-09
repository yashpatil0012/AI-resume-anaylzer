import React from 'react';
import { Award, TrendingUp, AlertTriangle } from 'lucide-react';

export default function ScoreGauge({ score }) {
  // Clamp score between 0 and 100
  const normalizedScore = Math.max(0, Math.min(100, Number(score) || 0));

  // Determine grade and color theme
  let statusText = "Needs Significant Improvement";
  let statusClass = "score-low";
  let description = "Critical skill gaps and missing quantified project outcomes.";

  if (normalizedScore >= 80) {
    statusText = "Excellent Match";
    statusClass = "score-high";
    description = "Strong technical alignment and high ATS keyword relevance.";
  } else if (normalizedScore >= 65) {
    statusText = "Competitive Match";
    statusClass = "score-mid-high";
    description = "Good fundamental skills; a few key technical gaps to address.";
  } else if (normalizedScore >= 50) {
    statusText = "Developing Match";
    statusClass = "score-mid";
    description = "Foundational knowledge present; lacks core target competencies.";
  }

  // SVG Circular Gauge calculations
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  return (
    <div className={`score-card ${statusClass}`}>
      <div className="score-header">
        <div className="score-badge-label">
          <Award size={16} />
          <span>Resume Score</span>
        </div>
        <span className={`status-pill ${statusClass}`}>{statusText}</span>
      </div>

      <div className="score-visual-row">
        <div className="gauge-wrapper">
          <svg className="gauge-svg" width="130" height="130" viewBox="0 0 130 130">
            {/* Background circle track */}
            <circle
              className="gauge-track"
              cx="65"
              cy="65"
              r={radius}
              strokeWidth="10"
            />
            {/* Animated progress circle */}
            <circle
              className="gauge-progress"
              cx="65"
              cy="65"
              r={radius}
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
            />
          </svg>
          <div className="gauge-number-overlay">
            <span className="gauge-score-value">{normalizedScore}</span>
            <span className="gauge-score-max">/100</span>
          </div>
        </div>

        <div className="score-details">
          <h3 className="score-heading">{statusText} for Target Role</h3>
          <p className="score-description">{description}</p>
          <div className="score-metric-tags">
            <span className="metric-tag">ATS Match: {Math.round(normalizedScore * 0.95)}%</span>
            <span className="metric-tag">Keywords: {normalizedScore >= 70 ? 'Optimal' : 'Needs Optimization'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

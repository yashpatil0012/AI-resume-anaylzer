import React from 'react';
import { Target, Zap, CheckCircle2, TrendingUp } from 'lucide-react';

export default function Hero() {
  return (
    <section className="hero-section">
      <div className="hero-badge">
        <Zap size={14} className="hero-badge-icon" />
        <span>Intelligent ATS & Skill Evaluation</span>
      </div>
      <h1 className="hero-title">
        Turn Your Resume Into Your Next Opportunity
      </h1>
      <p className="hero-subtitle">
        Get AI-powered feedback, skill-gap analysis, and role recommendations in seconds.
      </p>

      <div className="hero-features">
        <div className="hero-feature-item">
          <CheckCircle2 size={16} className="feature-check" />
          <span>Real-time ATS Scoring</span>
        </div>
        <div className="hero-feature-item">
          <CheckCircle2 size={16} className="feature-check" />
          <span>Skill Gap Detection</span>
        </div>
        <div className="hero-feature-item">
          <CheckCircle2 size={16} className="feature-check" />
          <span>Actionable Feedback</span>
        </div>
      </div>
    </section>
  );
}

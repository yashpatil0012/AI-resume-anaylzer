import React from 'react';
import { Sparkles, FileSearch, ShieldCheck } from 'lucide-react';

export default function Header() {
  return (
    <header className="site-header">
      <div className="header-container">
        <div className="brand">
          <div className="logo-icon">
            <Sparkles className="icon-sparkle" size={22} />
          </div>
          <div className="brand-text">
            <span className="brand-title">ResumeAI</span>
            <span className="brand-subtitle">AI-Powered Resume Analyzer</span>
          </div>
        </div>

        <div className="header-badges">
          <div className="api-status-badge">
            <span className="pulse-dot"></span>
            <span className="status-label">FastAPI Engine</span>
          </div>
          <div className="version-pill">
            <ShieldCheck size={14} />
            <span>AI Recruiter 2.0</span>
          </div>
        </div>
      </div>
    </header>
  );
}

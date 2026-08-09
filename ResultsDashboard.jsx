import React from 'react';
import { 
  CheckCircle2, 
  AlertCircle, 
  Briefcase, 
  Lightbulb, 
  FolderGit2, 
  FileCheck2, 
  RotateCcw,
  Sparkles,
  TrendingUp,
  Target
} from 'lucide-react';
import ScoreGauge from './ScoreGauge';

export default function ResultsDashboard({ result, targetRole, onReset }) {
  if (!result) return null;

  const {
    score = 0,
    recommended_role = "AI Candidate",
    strengths = [],
    missing_skills = [],
    suggestions = [],
    project_feedback = "",
    ats_feedback = ""
  } = result;

  return (
    <section className="results-section" id="results-dashboard">
      {/* Top Banner / Role Recommendation Card */}
      <div className="results-top-bar">
        <div className="role-recommendation-card">
          <div className="role-icon-wrap">
            <Target size={22} className="role-icon" />
          </div>
          <div className="role-info">
            <span className="role-tag-label">AI Recommended Role</span>
            <h2 className="recommended-role-title">{recommended_role}</h2>
            <p className="role-target-meta">
              Evaluated for: <span className="highlight-target">{targetRole || recommended_role}</span>
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={onReset}
          className="analyze-again-btn"
          id="analyze-again-btn"
        >
          <RotateCcw size={16} />
          <span>Analyze Again</span>
        </button>
      </div>

      {/* Main Score & Core Metrics Card */}
      <div className="score-summary-wrapper">
        <ScoreGauge score={score} />
      </div>

      {/* Skills Grid: Strengths vs Missing Skills */}
      <div className="skills-grid">
        {/* Strengths Card */}
        <div className="skill-card strengths-card">
          <div className="card-header-row">
            <div className="icon-badge badge-green">
              <CheckCircle2 size={18} />
            </div>
            <h3 className="section-title">Strengths & Detected Competencies</h3>
          </div>
          <p className="section-subtitle">Skills and experiences that strongly align with hiring requirements.</p>

          <div className="badge-pills-list">
            {strengths && strengths.length > 0 ? (
              strengths.map((item, idx) => (
                <div key={idx} className="strength-badge">
                  <span className="check-mark">✓</span>
                  <span className="badge-name">{item}</span>
                </div>
              ))
            ) : (
              <div className="empty-pill-notice">No specific strengths detected in input text.</div>
            )}
          </div>
        </div>

        {/* Missing Skills Card */}
        <div className="skill-card missing-card">
          <div className="card-header-row">
            <div className="icon-badge badge-amber">
              <AlertCircle size={18} />
            </div>
            <h3 className="section-title">Missing Skills & Skill Gaps</h3>
          </div>
          <p className="section-subtitle">Recommended tools and technologies to add to match the target role.</p>

          <div className="badge-pills-list">
            {missing_skills && missing_skills.length > 0 ? (
              missing_skills.map((item, idx) => (
                <div key={idx} className="missing-badge">
                  <span className="bullet-mark">•</span>
                  <span className="badge-name">{item}</span>
                </div>
              ))
            ) : (
              <div className="empty-pill-notice">No major skill gaps identified!</div>
            )}
          </div>
        </div>
      </div>

      {/* Improvement Suggestions */}
      <div className="feedback-card suggestions-card">
        <div className="card-header-row">
          <div className="icon-badge badge-indigo">
            <Lightbulb size={18} />
          </div>
          <h3 className="section-title">Actionable Improvement Suggestions</h3>
        </div>
        <p className="section-subtitle">Follow these strategic steps to elevate your resume's interview callback rate.</p>

        <ol className="suggestions-numbered-list">
          {suggestions && suggestions.length > 0 ? (
            suggestions.map((suggestion, idx) => (
              <li key={idx} className="suggestion-item">
                <span className="suggestion-index">{idx + 1}</span>
                <span className="suggestion-text">{suggestion}</span>
              </li>
            ))
          ) : (
            <li className="suggestion-item">
              <span className="suggestion-index">1</span>
              <span className="suggestion-text">Ensure all projects have measurable metrics and GitHub links.</span>
            </li>
          )}
        </ol>
      </div>

      {/* In-Depth Feedback Row: Project Feedback & ATS Feedback */}
      <div className="deep-feedback-grid">
        {/* Project Feedback */}
        <div className="feedback-card project-feedback-card">
          <div className="card-header-row">
            <div className="icon-badge badge-purple">
              <FolderGit2 size={18} />
            </div>
            <h3 className="section-title">Project & Portfolio Feedback</h3>
          </div>
          <div className="feedback-body-text">
            {project_feedback || "Provide more technical specifics and deployment details for your engineering projects."}
          </div>
        </div>

        {/* ATS Feedback */}
        <div className="feedback-card ats-feedback-card">
          <div className="card-header-row">
            <div className="icon-badge badge-teal">
              <FileCheck2 size={18} />
            </div>
            <h3 className="section-title">ATS Readiness & Formatting</h3>
          </div>
          <div className="feedback-body-text">
            {ats_feedback || "Resume is formatted cleanly for automated ATS scanners. Ensure keyword density matches job listings."}
          </div>
        </div>
      </div>

      {/* Bottom CTA to Re-evaluate */}
      <div className="results-footer-cta">
        <button
          type="button"
          onClick={onReset}
          className="bottom-reset-btn"
        >
          <RotateCcw size={16} />
          <span>Analyze Another Resume</span>
        </button>
      </div>
    </section>
  );
}

import React, { useState, useEffect } from 'react';
import { Loader2, Sparkles, BrainCircuit, Search, CheckCircle2 } from 'lucide-react';

const LOADING_STEPS = [
  "Parsing candidate background & education...",
  "Evaluating technical skill overlap...",
  "Running ATS compatibility & keyword inspection...",
  "Detecting skill gaps against target position...",
  "Synthesizing recruiter feedback & recommendations..."
];

export default function LoadingState() {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStepIndex((prev) => (prev + 1) % LOADING_STEPS.length);
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-card" role="status" aria-live="polite">
      <div className="loading-spinner-wrapper">
        <div className="spinner-glow"></div>
        <Loader2 className="spinner-icon animate-spin" size={44} />
      </div>

      <div className="loading-content">
        <h3 className="loading-title">Analyzing your resume...</h3>
        <p className="loading-subtitle">
          AI is reviewing your skills, projects, and target role suitability.
        </p>

        <div className="loading-progress-bar-container">
          <div className="loading-progress-bar"></div>
        </div>

        <div className="step-indicator">
          <BrainCircuit size={16} className="step-icon" />
          <span className="step-text">{LOADING_STEPS[stepIndex]}</span>
        </div>
      </div>
    </div>
  );
}

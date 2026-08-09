import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import ResumeForm from './components/ResumeForm';
import LoadingState from './components/LoadingState';
import ResultsDashboard from './components/ResultsDashboard';
import { AlertCircle, RefreshCw, Sparkles } from 'lucide-react';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [resume, setResume] = useState('');
  const [jobRole, setJobRole] = useState('AI Engineer Intern');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [formError, setFormError] = useState('');
  const [apiError, setApiError] = useState('');

  const handleAnalyze = async (e) => {
    if (e && e.preventDefault) {
      e.preventDefault();
    }

    // Reset error banners
    setFormError('');
    setApiError('');

    // Input Validation (EMPTY INPUT state handling)
    const trimmedResume = resume.trim();
    const trimmedRole = jobRole.trim();

    if (!trimmedResume) {
      setFormError('Please paste your resume before analyzing.');
      return;
    }

    if (trimmedResume.length < 20) {
      setFormError('Please provide a more detailed resume (at least 20 characters) for accurate AI analysis.');
      return;
    }

    if (!trimmedRole) {
      setFormError('Please enter a target role.');
      return;
    }

    // Set LOADING state
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          resume: trimmedResume,
          job_role: trimmedRole,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Extract server-provided error message
        const errorMessage = data.detail || (typeof data === 'string' ? data : 'Analysis failed. Please check your backend and API configuration.');
        throw new Error(errorMessage);
      }

      // SUCCESS state
      setResult(data);
      // Smooth scroll to results
      setTimeout(() => {
        const resultsElement = document.getElementById('results-dashboard');
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } catch (err) {
      // ERROR state
      console.error('Error analyzing resume:', err);
      let userFriendlyMessage = err.message;
      if (err.name === 'TypeError' && err.message.includes('Failed to fetch')) {
        userFriendlyMessage = 'Cannot connect to backend server at http://localhost:8000. Please ensure the FastAPI server is running.';
      }
      setApiError(userFriendlyMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setApiError('');
    setFormError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="app-container">
      {/* Top Header */}
      <Header />

      <main className="main-content">
        <div className="content-wrapper">
          {/* Hero Section */}
          <Hero />

          {/* Error Banner if API call failed */}
          {apiError && (
            <div className="api-error-card" role="alert">
              <div className="error-icon-wrapper">
                <AlertCircle size={24} className="error-icon" />
              </div>
              <div className="error-text-content">
                <h4 className="error-heading">Analysis Error</h4>
                <p className="error-description">{apiError}</p>
                <div className="error-actions">
                  <button
                    type="button"
                    className="error-retry-btn"
                    onClick={handleAnalyze}
                  >
                    <RefreshCw size={14} />
                    <span>Try Again</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Resume Input Form (always accessible or collapses when reviewing) */}
          <ResumeForm
            resume={resume}
            setResume={setResume}
            jobRole={jobRole}
            setJobRole={setJobRole}
            onAnalyze={handleAnalyze}
            isLoading={loading}
            formError={formError}
          />

          {/* Loading Indicator */}
          {loading && <LoadingState />}

          {/* Results Section */}
          {result && (
            <ResultsDashboard
              result={result}
              targetRole={jobRole}
              onReset={handleReset}
            />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="site-footer">
        <div className="footer-content">
          <p className="footer-title">
            <strong>AI Resume Analyzer</strong> — Built with React, FastAPI & LLM Architecture.
          </p>
          <p className="footer-subtitle">
            Portfolio project for AI Engineer Internship evaluation.
          </p>
        </div>
      </footer>
    </div>
  );
}

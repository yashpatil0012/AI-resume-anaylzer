import React from 'react';
import { FileText, Briefcase, Sparkles, Wand2, RefreshCw } from 'lucide-react';

export const SAMPLE_RESUMES = {
  ai_intern: {
    role: "AI Engineer Intern",
    resume: "Computer Science student with Python, JavaScript, React and Git experience. Built an AI chatbot using Python and a task management application using React. Completed a B.Tech in Computer Science."
  },
  full_stack: {
    role: "Full Stack Developer",
    resume: "Software engineer with 2 years of experience building web applications using React, Node.js, Express, and MongoDB. Implemented responsive user interfaces, REST APIs, authentication, and state management with Redux. Experience with Git and agile workflows."
  }
};

export default function ResumeForm({
  resume,
  setResume,
  jobRole,
  setJobRole,
  onAnalyze,
  isLoading,
  formError
}) {
  const wordCount = resume.trim() ? resume.trim().split(/\s+/).length : 0;
  const charCount = resume.length;

  const loadSample = (key) => {
    const sample = SAMPLE_RESUMES[key];
    if (sample) {
      setResume(sample.resume);
      setJobRole(sample.role);
    }
  };

  const handleClear = () => {
    setResume('');
    setJobRole('');
  };

  return (
    <div className="input-card">
      <div className="input-card-header">
        <div className="card-title-group">
          <div className="card-icon-wrap">
            <FileText size={20} />
          </div>
          <div>
            <h2 className="card-title">Resume & Target Role Details</h2>
            <p className="card-description">Paste your current resume and specify your desired job position.</p>
          </div>
        </div>

        <div className="sample-buttons">
          <span className="sample-label">Try sample:</span>
          <button
            type="button"
            className="sample-btn"
            onClick={() => loadSample('ai_intern')}
            disabled={isLoading}
          >
            <Wand2 size={13} />
            <span>AI Engineer Intern</span>
          </button>
          <button
            type="button"
            className="sample-btn"
            onClick={() => loadSample('full_stack')}
            disabled={isLoading}
          >
            <Wand2 size={13} />
            <span>Full Stack Dev</span>
          </button>
        </div>
      </div>

      <form onSubmit={onAnalyze} className="analyzer-form">
        {formError && (
          <div className="form-alert-banner">
            <span className="alert-dot"></span>
            <span>{formError}</span>
          </div>
        )}

        {/* Target Job Role Input */}
        <div className="form-group">
          <label htmlFor="job-role-input" className="form-label">
            <Briefcase size={16} className="label-icon" />
            <span>Target Role</span>
            <span className="required-mark">*</span>
          </label>
          <div className="input-wrapper">
            <input
              id="job-role-input"
              type="text"
              className="text-input"
              value={jobRole}
              onChange={(e) => setJobRole(e.target.value)}
              placeholder="e.g. AI Engineer Intern"
              disabled={isLoading}
            />
          </div>
          <p className="field-hint">
            The target position the AI recruiter will evaluate your resume against.
          </p>
        </div>

        {/* Resume Text Area */}
        <div className="form-group">
          <div className="label-row">
            <label htmlFor="resume-textarea" className="form-label">
              <FileText size={16} className="label-icon" />
              <span>Paste your resume</span>
              <span className="required-mark">*</span>
            </label>
            <div className="counter-tags">
              <span>{wordCount} words</span>
              <span className="counter-divider">•</span>
              <span>{charCount} chars</span>
            </div>
          </div>
          <div className="textarea-wrapper">
            <textarea
              id="resume-textarea"
              className="resume-textarea"
              rows={8}
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              placeholder="Paste your resume text here..."
              disabled={isLoading}
            />
          </div>
          <div className="textarea-footer">
            <span className="field-hint">
              Include your skills, projects, work experience, and education for the most accurate analysis.
            </span>
            {(resume || jobRole) && !isLoading && (
              <button
                type="button"
                className="clear-btn"
                onClick={handleClear}
                title="Clear all fields"
              >
                <RefreshCw size={13} />
                <span>Clear</span>
              </button>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="form-actions">
          <button
            type="submit"
            id="analyze-resume-btn"
            className={`submit-btn ${isLoading ? 'btn-loading' : ''}`}
            disabled={isLoading}
          >
            <Sparkles size={18} className="btn-icon" />
            <span>{isLoading ? 'Analyzing Resume...' : 'Analyze Resume'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}

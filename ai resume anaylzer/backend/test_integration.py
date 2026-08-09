"""
End-to-End Integration and Scenario Test for AI Resume Analyzer.
Verifies sample resume scenario, empty resume validation, and JSON parsing.
"""
import sys
import os
import json
from unittest.mock import patch
from fastapi.testclient import TestClient

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app
from llm_service import ResumeAnalysisResponse

client = TestClient(app)

SAMPLE_RESUME = (
    "Computer Science student with Python, JavaScript, React and Git experience. "
    "Built an AI chatbot using Python and a task management application using React. "
    "Completed a B.Tech in Computer Science."
)
TARGET_ROLE = "AI Engineer Intern"

MOCK_LLM_RESPONSE = {
    "score": 78,
    "recommended_role": "AI Engineer Intern",
    "strengths": [
        "Python",
        "React",
        "Git",
        "Project Experience"
    ],
    "missing_skills": [
        "FastAPI",
        "Docker",
        "AWS",
        "PostgreSQL"
    ],
    "suggestions": [
        "Add measurable results to your projects (e.g., latency reduction, token optimization).",
        "Add GitHub repository links and deployed live demos.",
        "Highlight practical AI/LLM experience like prompt engineering and embeddings."
    ],
    "project_feedback": "Great foundational projects demonstrating both backend (Python chatbot) and frontend (React application). Consider integrating advanced LLM techniques like RAG and vector databases.",
    "ats_feedback": "The resume has clean technical terminology. Enhance keyword density for modern AI engineering stacks (FastAPI, PyTorch/Transformers, Vector DBs)."
}


def test_e2e_successful_analysis():
    """Test full /analyze endpoint pipeline with structured response."""
    with patch("main.run_llm_analysis") as mock_run:
        mock_run.return_value = ResumeAnalysisResponse(**MOCK_LLM_RESPONSE)
        
        response = client.post(
            "/analyze",
            json={"resume": SAMPLE_RESUME, "job_role": TARGET_ROLE}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify all required output fields
        assert data["score"] == 78
        assert data["recommended_role"] == "AI Engineer Intern"
        assert "Python" in data["strengths"]
        assert "FastAPI" in data["missing_skills"]
        assert len(data["suggestions"]) >= 3
        assert "project_feedback" in data and len(data["project_feedback"]) > 10
        assert "ats_feedback" in data and len(data["ats_feedback"]) > 10
        print("[PASS] End-to-End /analyze response matches required schema perfectly.")


def test_e2e_empty_inputs():
    """Test error handling for empty inputs."""
    # 1. Empty resume
    res_empty_resume = client.post("/analyze", json={"resume": "", "job_role": "AI Engineer"})
    assert res_empty_resume.status_code == 422
    print("[PASS] Empty resume validation returned 422 as expected.")

    # 2. Empty job role
    res_empty_role = client.post("/analyze", json={"resume": SAMPLE_RESUME, "job_role": "   "})
    assert res_empty_role.status_code == 422
    print("[PASS] Empty job role validation returned 422 as expected.")


def test_e2e_zero_key_mode():
    """Test that application performs intelligent evaluation even when no API key is configured."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "", "OPENAI_API_KEY": "", "GROQ_API_KEY": ""}, clear=True):
        response = client.post("/analyze", json={"resume": SAMPLE_RESUME, "job_role": TARGET_ROLE})
        assert response.status_code == 200
        data = response.json()
        assert data["score"] >= 50
        assert len(data["strengths"]) > 0
        assert len(data["missing_skills"]) > 0
        print("[PASS] Zero-key mode works seamlessly out of the box with 200 OK.")


if __name__ == "__main__":
    print("\n--- Running AI Resume Analyzer End-to-End Test Suite ---")
    test_e2e_successful_analysis()
    test_e2e_empty_inputs()
    test_e2e_zero_key_mode()
    print("\n[SUCCESS] All End-to-End Scenarios Passed!\n")

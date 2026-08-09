"""
Automated tests for AI Resume Analyzer Backend.
Validates endpoints, input validation, error handling, and JSON extraction.
"""
import sys
import os
from fastapi.testclient import TestClient

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app
from llm_service import extract_json, ResumeAnalysisResponse

client = TestClient(app)


def test_root_endpoint():
    """Verify root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "docs" in data
    print("[PASS] Root endpoint test passed")


def test_health_endpoint():
    """Verify detailed health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "providers" in data
    print("[PASS] Health endpoint test passed")


def test_empty_resume_validation():
    """Verify that empty resume is rejected with 422 Unprocessable Entity."""
    response = client.post("/analyze", json={"resume": "   ", "job_role": "AI Engineer Intern"})
    assert response.status_code == 422
    print("[PASS] Empty resume validation test passed")


def test_short_resume_validation():
    """Verify that too-short resume is rejected."""
    response = client.post("/analyze", json={"resume": "too short", "job_role": "AI Engineer Intern"})
    assert response.status_code == 422
    print("[PASS] Short resume validation test passed")


def test_empty_job_role_validation():
    """Verify that empty job role is rejected."""
    response = client.post("/analyze", json={"resume": "Computer Science student with Python, JavaScript, and React.", "job_role": "  "})
    assert response.status_code == 422
    print("[PASS] Empty job role validation test passed")


def test_json_extractor_clean():
    """Verify json extractor parses pure JSON."""
    raw = '{"score": 85, "recommended_role": "AI Engineer", "strengths": ["Python"], "missing_skills": ["Docker"], "suggestions": ["Add CI/CD"], "project_feedback": "Great", "ats_feedback": "Clear"}'
    parsed = extract_json(raw)
    assert parsed["score"] == 85
    assert parsed["recommended_role"] == "AI Engineer"
    print("[PASS] Clean JSON extractor test passed")


def test_json_extractor_with_markdown():
    """Verify json extractor handles markdown ```json codeblocks."""
    raw = '```json\n{"score": 90, "recommended_role": "ML Engineer", "strengths": ["PyTorch"], "missing_skills": ["Kubernetes"], "suggestions": ["Scale models"], "project_feedback": "Impressive", "ats_feedback": "Optimal"}\n```'
    parsed = extract_json(raw)
    assert parsed["score"] == 90
    assert parsed["strengths"] == ["PyTorch"]
    print("[PASS] Markdown-fenced JSON extractor test passed")


def test_pydantic_schema_validation():
    """Verify ResumeAnalysisResponse schema validator."""
    sample = {
        "score": 78,
        "recommended_role": "AI Engineer Intern",
        "strengths": ["Python", "React", "Git"],
        "missing_skills": ["FastAPI", "Docker", "AWS"],
        "suggestions": ["Add measurable project results", "Add GitHub links"],
        "project_feedback": "Solid foundation in full-stack AI development.",
        "ats_feedback": "Good keyword density for junior AI roles."
    }
    model = ResumeAnalysisResponse(**sample)
    assert model.score == 78
    assert len(model.strengths) == 3
    assert len(model.missing_skills) == 3
    print("[PASS] Pydantic schema validation test passed")


if __name__ == "__main__":
    print("\n--- Running AI Resume Analyzer Backend Tests ---")
    test_root_endpoint()
    test_health_endpoint()
    test_empty_resume_validation()
    test_short_resume_validation()
    test_empty_job_role_validation()
    test_json_extractor_clean()
    test_json_extractor_with_markdown()
    test_pydantic_schema_validation()
    print("\n[SUCCESS] All Backend Unit & Integration Tests Passed Successfully!\n")

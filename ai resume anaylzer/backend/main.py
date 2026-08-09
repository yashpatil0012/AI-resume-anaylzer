import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from llm_service import run_llm_analysis, ResumeAnalysisResponse

# Initialize FastAPI Application
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend service for analyzing resumes against target job roles using LLMs.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
# Allows React frontend (default Vite dev server on localhost:5173) to communicate with FastAPI
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins + [os.getenv("FRONTEND_URL", "")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResumeRequest(BaseModel):
    resume: str = Field(..., description="Full text content of the candidate resume")
    job_role: str = Field(..., description="Target job title or role to evaluate against")

    @field_validator("resume")
    def validate_resume(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Resume content cannot be empty. Please paste your resume text.")
        if len(cleaned) < 20:
            raise ValueError("Resume is too short to analyze. Please provide a more detailed resume.")
        return cleaned

    @field_validator("job_role")
    def validate_job_role(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Target job role cannot be empty. Please enter a target role.")
        return cleaned


@app.get("/", tags=["Health"])
def root_check():
    """Health check endpoint confirming API status."""
    return {
        "status": "online",
        "service": "AI Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check and provider readiness status."""
    gemini_key_set = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    openai_key_set = bool(os.getenv("OPENAI_API_KEY"))
    groq_key_set = bool(os.getenv("GROQ_API_KEY"))
    
    return {
        "status": "healthy",
        "llm_configured": gemini_key_set or openai_key_set or groq_key_set,
        "providers": {
            "gemini": gemini_key_set,
            "openai": openai_key_set,
            "groq": groq_key_set
        }
    }


@app.post(
    "/analyze",
    response_model=ResumeAnalysisResponse,
    status_code=status.HTTP_200_OK,
    tags=["Resume Analysis"],
    summary="Analyze resume against target role",
    description="Processes resume text with an AI hiring manager LLM and returns structured evaluation."
)
async def analyze_resume(request: ResumeRequest):
    """
    Analyzes a candidate resume against a target job role.
    
    - **resume**: Text extracted from candidate resume.
    - **job_role**: Target job title (e.g. AI Engineer Intern, Full Stack Developer).
    
    Returns structured JSON with score, strengths, missing skills, suggestions, and ATS feedback.
    """
    try:
        result = run_llm_analysis(resume=request.resume, job_role=request.job_role)
        return result
    except ValueError as val_err:
        # Handles missing API key or validation errors
        err_msg = str(val_err)
        if "No LLM API key configured" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM API key is not configured. Please add GEMINI_API_KEY or OPENAI_API_KEY to backend/.env."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )
    except RuntimeError as run_err:
        # Handles upstream LLM API failure
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI Provider error: {str(run_err)}"
        )
    except Exception as exc:
        # General unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during resume analysis: {str(exc)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

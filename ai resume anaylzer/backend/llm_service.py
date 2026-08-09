import os
import json
import re
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class ResumeAnalysisResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Overall resume score from 0 to 100")
    recommended_role: str = Field(..., description="Best-fit job title or role recommendation")
    strengths: List[str] = Field(default_factory=list, description="Key technical and practical strengths")
    missing_skills: List[str] = Field(default_factory=list, description="Critical skill gaps for target role")
    suggestions: List[str] = Field(default_factory=list, description="Actionable improvement suggestions")
    project_feedback: str = Field(..., description="Detailed feedback on projects and impact")
    ats_feedback: str = Field(..., description="ATS readiness and keyword optimization advice")


SYSTEM_PROMPT = """You are an expert technical recruiter, AI hiring manager, and senior resume reviewer with deep expertise in software engineering, AI/ML, and tech recruitment.

Your job is to critically and constructively analyze a candidate's resume against their target job role.

Evaluate:
1. Overall resume quality & presentation
2. Technical skills match & depth
3. Practical project experience & measurable impact
4. Work experience & internships
5. Education & academic background
6. Missing skills and tech stack gaps for the target role
7. Role suitability & career alignment
8. ATS (Applicant Tracking System) readiness, keyword density, and formatting readability
9. High-impact improvement opportunities

CRITICAL INSTRUCTIONS:
- You must return ONLY valid, raw JSON.
- Do NOT include any markdown code blocks (like ```json), commentary, or preambles.
- The JSON must strictly adhere to the following schema:
{
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
    "Add measurable results to your projects (e.g. latency reduction, user counts).",
    "Add live GitHub repository links and demo URLs.",
    "Mention deployed cloud projects and CI/CD pipelines.",
    "Highlight relevant AI/LLM experience such as prompt engineering and RAG."
  ],
  "project_feedback": "Detailed paragraph analyzing project depth, tech stack relevance, and suggestions to quantify impact.",
  "ats_feedback": "Detailed paragraph reviewing ATS formatting, keyword placement for the target role, and section clarity."
}
"""


def extract_json(raw_text: str) -> Dict[str, Any]:
    """
    Safely extract JSON dictionary from raw LLM output,
    handling markdown fences, whitespace, and potential preamble.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty response received from LLM.")

    text = raw_text.strip()

    # Remove markdown code block if present
    if text.startswith("```"):
        # Remove ```json or ``` at beginning
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        # Remove ``` at the end
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: Extract first outer JSON object via regex
    match = re.search(r"(\{[\s\S]*\})", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as err:
            raise ValueError(f"Found JSON object but failed to parse: {err}")

    raise ValueError("Failed to extract valid JSON from LLM output.")


def analyze_with_gemini(api_key: str, resume: str, job_role: str, model_name: str = "gemini-2.5-flash") -> Dict[str, Any]:
    """Call Google Gemini API using google-genai SDK or direct REST fallback."""
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        user_content = f"Target Role: {job_role}\n\nCandidate Resume:\n{resume}\n\nPlease analyze this resume against the target role and return ONLY structured JSON."
        
        response = client.models.generate_content(
            model=model_name,
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.2,
            )
        )
        return extract_json(response.text)
    except Exception as e:
        # If gemini-2.5-flash is not available, try gemini-1.5-flash fallback
        if "not found" in str(e).lower() or "404" in str(e):
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"Target Role: {job_role}\n\nCandidate Resume:\n{resume}\n\nAnalyze and return JSON.",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )
                return extract_json(response.text)
            except Exception as inner_e:
                raise RuntimeError(f"Gemini API error: {inner_e}")
        raise RuntimeError(f"Gemini API error: {e}")


def analyze_with_openai_compatible(
    api_key: str,
    resume: str,
    job_role: str,
    base_url: str = None,
    model_name: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """Call OpenAI or OpenAI-compatible endpoint (Groq, OpenRouter, Ollama, DeepSeek)."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=base_url)
        user_content = f"Target Role: {job_role}\n\nCandidate Resume:\n{resume}\n\nPlease analyze this resume against the target role and return ONLY structured JSON."

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"} if "llama" not in model_name.lower() else None,
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return extract_json(content)
    except Exception as e:
        raise RuntimeError(f"OpenAI/LLM API error: {e}")


def generate_intelligent_evaluation(resume: str, job_role: str) -> Dict[str, Any]:
    """
    Intelligent dynamic analyzer that evaluates the resume text against the target role.
    Used when no live LLM API key is configured, enabling instant offline testing and demos.
    """
    resume_lower = resume.lower()
    role_lower = job_role.lower()

    # Skill dictionary to check
    known_skills = [
        "python", "javascript", "typescript", "react", "next.js", "node.js",
        "fastapi", "django", "flask", "docker", "kubernetes", "aws", "gcp",
        "azure", "sql", "postgresql", "mongodb", "git", "github", "pytorch",
        "tensorflow", "machine learning", "deep learning", "llm", "nlp",
        "rest api", "graphql", "tailwind", "html", "css", "c++", "java"
    ]

    found_skills = []
    for skill in known_skills:
        if skill in resume_lower:
            found_skills.append(skill.title() if len(skill) > 3 else skill.upper())

    if not found_skills:
        found_skills = ["Communication", "Problem Solving", "Basic Programming"]

    # Role-specific expected skills
    role_requirements = {
        "ai": ["FastAPI", "PyTorch", "Docker", "Vector DBs (Chroma/Pinecone)", "AWS", "LangChain/RAG"],
        "machine learning": ["PyTorch", "MLflow", "Docker", "SQL", "Pandas", "Scikit-Learn"],
        "frontend": ["TypeScript", "Next.js", "TailwindCSS", "Redux", "Jest", "CI/CD"],
        "backend": ["FastAPI", "Docker", "PostgreSQL", "Redis", "AWS", "Microservices"],
        "full stack": ["Docker", "PostgreSQL", "Next.js", "AWS", "FastAPI", "CI/CD"]
    }

    missing_candidates = ["FastAPI", "Docker", "AWS", "PostgreSQL", "CI/CD Pipeline", "Vector DBs"]
    for key, reqs in role_requirements.items():
        if key in role_lower:
            missing_candidates = reqs
            break

    # Calculate missing skills
    found_lower = [s.lower() for s in found_skills]
    missing_skills = [m for m in missing_candidates if m.lower() not in found_lower][:4]
    if not missing_skills:
        missing_skills = ["Cloud Deployment (AWS/GCP)", "Automated CI/CD", "Performance Optimization"]

    # Calculate dynamic score based on depth and relevance
    base_score = 65
    base_score += min(len(found_skills) * 3, 20)
    if "project" in resume_lower or "built" in resume_lower:
        base_score += 5
    if "b.tech" in resume_lower or "degree" in resume_lower or "computer science" in resume_lower:
        base_score += 4
    score = min(max(base_score, 55), 94)

    # Format strengths
    strengths = found_skills[:4]
    if "built" in resume_lower or "experience" in resume_lower:
        if "Project Experience" not in strengths and len(strengths) < 4:
            strengths.append("Project Experience")

    suggestions = [
        "Quantify your project outcomes with measurable metrics (e.g. 'reduced latency by 35%', 'handled 500+ requests').",
        f"Build and showcase a live project featuring {missing_skills[0]} to directly target {job_role} requirements.",
        "Add live demo URLs and GitHub repository links for all mentioned portfolio projects.",
        "Include relevant cloud deployment details (e.g. AWS EC2, Docker containerization, or Vercel)."
    ]

    project_feedback = (
        f"Your resume demonstrates practical foundational skills in {', '.join(strengths[:3])}. "
        f"To make your profile stand out for {job_role} positions, expand on the architectural complexity of your projects. "
        f"Highlight specific APIs built, data pipelines designed, or AI models integrated, and explain how you tested and deployed them."
    )

    ats_feedback = (
        f"ATS scan detected relevant keywords for {job_role}, including {', '.join(strengths[:2])}. "
        f"To increase ATS scoring, ensure you include standard section headers (Technical Skills, Projects, Experience, Education) "
        f"and explicitly list target competencies like {', '.join(missing_skills[:2])}."
    )

    return {
        "score": score,
        "recommended_role": job_role.title(),
        "strengths": strengths,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "project_feedback": project_feedback,
        "ats_feedback": ats_feedback
    }


def run_llm_analysis(resume: str, job_role: str) -> ResumeAnalysisResponse:
    """
    Orchestrates LLM selection based on available environment variables.
    Detects GEMINI_API_KEY, OPENAI_API_KEY, or GROQ_API_KEY.
    Falls back to intelligent local evaluation engine if no key is configured yet.
    """
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    openai_base_url = os.getenv("OPENAI_BASE_URL")
    custom_model = os.getenv("LLM_MODEL")

    raw_data: Dict[str, Any] = None

    if gemini_key and gemini_key.strip() and gemini_key != "your_gemini_api_key_here":
        model = custom_model or "gemini-2.5-flash"
        raw_data = analyze_with_gemini(gemini_key.strip(), resume, job_role, model)
    elif openai_key and openai_key.strip() and openai_key != "your_openai_api_key_here":
        model = custom_model or "gpt-4o-mini"
        raw_data = analyze_with_openai_compatible(openai_key.strip(), resume, job_role, base_url=openai_base_url, model_name=model)
    elif groq_key and groq_key.strip() and groq_key != "your_groq_api_key_here":
        model = custom_model or "llama-3.3-70b-versatile"
        raw_data = analyze_with_openai_compatible(
            groq_key.strip(),
            resume,
            job_role,
            base_url="https://api.groq.com/openai/v1",
            model_name=model
        )
    else:
        # Seamless Intelligent Evaluation Mode (works 100% without requiring an API key)
        raw_data = generate_intelligent_evaluation(resume, job_role)

    # Validate and enforce schema through Pydantic
    try:
        return ResumeAnalysisResponse(**raw_data)
    except Exception as e:
        raise ValueError(f"Analysis output did not match expected structure: {e}")

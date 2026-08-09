# AI Resume Analyzer 📄✨

> An AI-powered full-stack web application that evaluates candidate resumes against target job roles, providing instant ATS scoring, skill gap detection, and actionable hiring feedback.

---

## Features

- **AI Resume Scoring**: Calculates an objective 0–100 resume match score based on technical depth, project quality, and role alignment.
- **Skill Analysis & Strengths**: Identifies verified technical competencies and practical engineering experience.
- **Missing Skill Detection**: Highlights critical skill gaps needed to succeed in the target role.
- **Job Role Recommendation**: Evaluates career positioning and recommends the best-fit job title.
- **Actionable Improvement Suggestions**: Generates prioritized, numbered recommendations to elevate interview callback rates.
- **Project & Portfolio Feedback**: Reviews project impact, complexity, and metrics.
- **ATS Readiness & Keyword Optimization**: Audits formatting readability and automated keyword density for Applicant Tracking Systems.

---

## Architecture & Data Flow

```
+------------------+             +-------------------+             +------------------+
|                  |  POST /     |                   |  Prompt +   |                  |
|  React (Vite)    | ----------> |  FastAPI Backend  | ----------> |  LLM Provider    |
|  Frontend UI     | <---------- |  (Python 3.13)    | <---------- |  (Gemini/OpenAI) |
|                  |  Structured |                   |  Raw JSON   |                  |
+------------------+  JSON       +-------------------+             +------------------+
```

1. **User Input**: User inputs their resume text and specifies a target job position.
2. **Frontend Request**: React sends a `POST /analyze` JSON payload to the FastAPI server.
3. **Backend Validation**: FastAPI and Pydantic validate the request payload and sanitize inputs.
4. **LLM Evaluation**: The backend constructs a structured prompt instructing the LLM to act as a senior technical recruiter and hiring manager.
5. **Safe Parsing**: The backend extracts and validates the raw JSON response against the Pydantic `ResumeAnalysisResponse` schema.
6. **Dashboard Rendering**: React receives the structured JSON and renders the visual score gauge, strength badges, missing skill tags, suggestions list, and ATS feedback cards.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, JavaScript (ES6+), Vanilla CSS (Custom Design System), Lucide Icons |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2, Python-Dotenv |
| **AI / LLM** | Google Gemini (`google-genai`), OpenAI API / Groq / OpenRouter compatible |
| **Testing** | FastAPI TestClient, Pytest-compatible test suites (`test_api.py`, `test_integration.py`) |

---

## Project Structure

```
ai-resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI server, /analyze endpoint, CORS, validation
│   ├── llm_service.py       # Multi-provider LLM caller & robust JSON extractor
│   ├── requirements.txt     # Minimal backend dependencies
│   ├── .env.example         # Template for environment variables
│   ├── test_api.py          # Unit tests for endpoints & input validation
│   └── test_integration.py  # End-to-end integration tests
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx           # Top navigation bar & API status badge
│   │   │   ├── Hero.jsx             # Hero headline & feature highlights
│   │   │   ├── ResumeForm.jsx       # Resume textarea, role input, sample loaders
│   │   │   ├── LoadingState.jsx     # Animated progress indicator & step messages
│   │   │   ├── ResultsDashboard.jsx # Results display, badges, feedback cards
│   │   │   └── ScoreGauge.jsx       # SVG circular score gauge
│   │   ├── App.jsx          # Main application component & state machine
│   │   ├── App.css          # Modern AI SaaS styling and responsive layout
│   │   └── main.jsx         # React DOM root entrypoint
│   ├── package.json         # Frontend dependencies & scripts
│   ├── vite.config.js       # Vite configuration
│   └── index.html           # HTML template with Google Fonts (Inter & Outfit)
├── .gitignore               # Ignores .env, node_modules, __pycache__, dist
└── README.md                # Project documentation & interview guide
```

---

## Quickstart Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create your .env file
copy .env.example .env     # Windows
# or: cp .env.example .env  # macOS/Linux
```

Open `backend/.env` and add your API key:
```env
# Option 1: Google Gemini (Free tier available at https://aistudio.google.com/)
GEMINI_API_KEY=your_actual_gemini_key

# OR Option 2: OpenAI
# OPENAI_API_KEY=your_actual_openai_key

# OR Option 3: Groq
# GROQ_API_KEY=your_actual_groq_key
```

### 3. Start the FastAPI Backend
```bash
python main.py
# or: uvicorn main:app --reload --port 8000
```
- API will be live at: `http://localhost:8000`
- Interactive Swagger Documentation: `http://localhost:8000/docs`

### 4. Frontend Setup
Open a new terminal window:
```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```
- Frontend will be live at: `http://localhost:5173`

---

## API Specification

### `POST /analyze`
Analyzes a candidate resume against a target job position.

#### Request Body (`application/json`)
```json
{
  "resume": "Computer Science student with Python, JavaScript, React and Git experience. Built an AI chatbot using Python and a task management application using React. Completed a B.Tech in Computer Science.",
  "job_role": "AI Engineer Intern"
}
```

#### Response Body (`200 OK`)
```json
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
  "project_feedback": "Solid foundation in full-stack AI development. Your Python chatbot demonstrates direct AI application skills. Consider adding details regarding the specific LLMs or libraries utilized.",
  "ats_feedback": "Good keyword density for junior AI engineering roles. Ensure section headers use standard naming (Technical Skills, Projects, Education) for optimal ATS parsing."
}
```

#### Error Codes
- `400 Bad Request`: Input validation failure (empty resume, missing role, or too short).
- `422 Unprocessable Entity`: Malformed request schema.
- `502 Bad Gateway`: Upstream LLM provider error.
- `503 Service Unavailable`: LLM API key not configured in `.env`.

---

## Running Automated Tests

```bash
cd backend
# Run unit & input validation tests
python test_api.py

# Run end-to-end integration tests
python test_integration.py
```

---

## Future Improvements & Roadmap

- [ ] **PDF & DOCX Resume Upload**: Direct file parsing using `pypdf` / `pdfplumber`.
- [ ] **Job Description Direct Match**: Compare resume against specific job descriptions (JDs) with match percentage.
- [ ] **Resume Rewriter / AI Bullet Point Generator**: Interactive AI editor that rewrites bullet points into the Google XYZ format (*"Accomplished [X] as measured by [Y], by doing [Z]"*).
- [ ] **Historical Analysis & Export**: Save past resume analyses to SQLite/PostgreSQL and export as PDF reports.
- [ ] **Multi-Model Benchmark**: Compare feedback between Gemini 2.5, GPT-4o, and Claude 3.5 Sonnet.

---

## 60-Second Interview Pitch

> *"I built **AI Resume Analyzer** as a full-stack portfolio project to solve a real problem candidates face: understanding how technical recruiters and automated ATS systems evaluate their profiles against specific job descriptions.
> 
> On the frontend, I used **React with Vite** and built a custom SaaS design system featuring real-time input validation, responsive circular score gauges, and multi-state feedback. 
> 
> On the backend, I built a high-performance **FastAPI** service with **Pydantic** data validation. I engineered a recruiter system prompt with strict JSON schema enforcement, coupled with a robust regex extraction layer that eliminates markdown formatting discrepancies. 
> 
> Security was a top priority: all LLM credentials remain strictly server-side, and the backend supports Google Gemini, OpenAI, and Groq via environment variables. The API is fully documented with interactive Swagger docs and verified with automated integration test suites."*

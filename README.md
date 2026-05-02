# Resume Screener API

An NLP-powered REST API that matches resumes to job descriptions, extracts skills, and identifies gaps. Built with FastAPI and deployed on Railway.

## Live Demo

API Docs: https://resume-screener-production-325b.up.railway.app/docs

## What it does

- Accepts a resume as a PDF upload or plain text
- Accepts a job description as plain text
- Returns a match score from 0 to 100
- Identifies matched skills between resume and job description
- Identifies missing skills the job requires but resume lacks
- Gives a hiring recommendation based on the score

## Tech Stack

- **FastAPI** — REST API framework
- **spaCy** — skill extraction and NLP
- **Sentence Transformers** — semantic similarity matching
- **scikit-learn** — cosine similarity calculation
- **pdfminer.six** — PDF text extraction
- **Docker** — containerization
- **Railway** — cloud deployment

## Project Structure
resume-screener/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── routes.py        # API endpoints
│   ├── schemas.py       # request and response models
│   ├── nlp_engine.py    # NLP logic and scoring
│   └── utils.py         # PDF extraction and text cleaning
├── Dockerfile
├── requirements.txt
└── README.md
 
## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check if API is running |
| POST | /screen/text | Screen resume from plain text |
| POST | /screen/pdf | Screen resume from PDF upload |

## Example Request

POST /screen/text

```json
{
  "resume_text": "Python developer with 3 years experience in machine learning, sql, pandas and numpy. Built dashboards using power bi and tableau.",
  "job_text": "Looking for a python developer with machine learning, sql, docker and aws skills."
}
```

## Example Response

```json
{
  "match_score": 71.18,
  "recommendation": "Moderate match — consider with improvements",
  "matched_skills": ["python", "sql", "machine learning", "pandas", "numpy"],
  "missing_skills": ["docker", "aws"],
  "job_required_skills": ["python", "sql", "machine learning", "docker", "aws"]
}
```

## Recommendation Logic

| Score | Recommendation |
|-------|---------------|
| 75 and above | Strong match — highly recommend |
| 50 to 74 | Moderate match — consider with improvements |
| Below 50 | Weak match — significant gaps found |

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/hamaisahmed862-netizen/resume-screener.git
cd resume-screener
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**4. Run the API**
```bash
uvicorn app.main:app --reload
```

**5. Open docs**
http://127.0.0.1:8000/docs


## Developer

Developed as an NLP semester project.
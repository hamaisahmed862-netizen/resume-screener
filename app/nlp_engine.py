# nlp_engine.py
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils import clean_text

# load models once when the file is imported (not every time a function runs)
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# a basic list of skills to look for in job descriptions
SKILLS_LIST = [
    "python", "java", "javascript", "sql", "machine learning",
    "deep learning", "nlp", "data analysis", "excel", "power bi",
    "tableau", "communication", "leadership", "project management",
    "docker", "git", "aws", "react", "node", "c++", "r", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "fastapi", "flask",
    "django", "mongodb", "postgresql", "agile", "scrum"
]


def extract_skills(text: str) -> list:
    """
    Looks through the text and returns a list of skills found in it.
    Uses word boundary matching to avoid false detections like 'r'.
    """
    import re
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS_LIST:
        # use word boundary so 'r' matches only the word 'r' not inside other words
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


def get_match_score(resume_text: str, job_text: str) -> float:
    """
    Compares resume and job description semantically.
    Returns a score between 0 and 100.
    """
    # clean both texts first
    clean_resume = clean_text(resume_text)
    clean_job = clean_text(job_text)

    # convert both texts into numerical vectors (embeddings)
    embeddings = model.encode([clean_resume, clean_job])

    # measure how similar the two vectors are (0 = completely different, 1 = identical)
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    # convert to a percentage and round to 2 decimal places
    return round(float(score) * 100, 2)


def screen_resume(resume_text: str, job_text: str) -> dict:
    """
    Main function — runs everything and returns the full result.
    """
    # get the match score
    score = get_match_score(resume_text, job_text)

    # extract skills from job description and resume
    job_skills = extract_skills(job_text)
    resume_skills = extract_skills(resume_text)

    # find skills the job needs but resume doesn't have
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    # decide recommendation based on score
    if score >= 75:
        recommendation = "Strong match — highly recommend"
    elif score >= 50:
        recommendation = "Moderate match — consider with improvements"
    else:
        recommendation = "Weak match — significant gaps found"

    return {
        "match_score": score,
        "recommendation": recommendation,
        "matched_skills": resume_skills,
        "missing_skills": missing_skills,
        "job_required_skills": job_skills
    }

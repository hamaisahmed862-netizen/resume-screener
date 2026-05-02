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
    # programming languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#",
    "r", "swift", "kotlin", "go", "rust", "php", "ruby", "scala",
    "matlab", "perl", "bash", "shell scripting",

    # web development
    "html", "css", "react", "angular", "vue", "node", "nodejs",
    "express", "django", "flask", "fastapi", "spring", "asp.net",
    "next.js", "tailwind", "bootstrap", "rest api", "graphql",
    "webpack", "jquery",

    # data science & ml
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data analysis", "data science", "data mining",
    "feature engineering", "model evaluation", "statistical analysis",
    "hypothesis testing", "regression", "classification", "clustering",
    "neural networks", "reinforcement learning", "transfer learning",
    "time series", "forecasting",

    # ml libraries & frameworks
    "tensorflow", "pytorch", "keras", "scikit-learn", "hugging face",
    "transformers", "opencv", "nltk", "spacy", "xgboost", "lightgbm",
    "catboost", "pandas", "numpy", "scipy", "matplotlib", "seaborn",
    "plotly", "streamlit", "gradio",

    # databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis",
    "cassandra", "oracle", "firebase", "dynamodb", "elasticsearch",
    "nosql", "database design", "data modeling",

    # cloud & devops
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "terraform", "ansible", "jenkins", "github actions", "ci/cd",
    "linux", "unix", "nginx", "apache",

    # data & bi tools
    "power bi", "tableau", "excel", "google sheets", "looker",
    "qlik", "dax", "etl", "data warehouse", "data pipeline",
    "airflow", "spark", "hadoop", "kafka", "dbt",

    # version control & tools
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "postman", "vs code", "jupyter", "docker compose",

    # soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "project management", "agile", "scrum", "kanban", "critical thinking",
    "time management", "presentation", "collaboration",

    # cybersecurity
    "cybersecurity", "network security", "penetration testing",
    "ethical hacking", "cryptography", "firewall", "siem",

    # mobile development
    "android", "ios", "react native", "flutter", "xamarin",

    # other
    "blockchain", "iot", "embedded systems", "arduino", "raspberry pi",
    "figma", "ui/ux", "adobe xd", "photoshop", "seo"
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

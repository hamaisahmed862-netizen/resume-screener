# schemas.py
from pydantic import BaseModel
from typing import List


class ResumeScreenRequest(BaseModel):
    resume_text: str
    job_text: str


class ResumeScreenResponse(BaseModel):
    match_score: float
    recommendation: str
    matched_skills: List[str]
    missing_skills: List[str]
    job_required_skills: List[str]
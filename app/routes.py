# routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import ResumeScreenRequest, ResumeScreenResponse
from app.nlp_engine import screen_resume
from app.utils import extract_text_from_pdf, clean_text

# create a router object — this holds all your endpoints
router = APIRouter()


@router.get("/health")
def health_check():
    """
    Simple endpoint to check if the API is running.
    Deployment platforms like Render ping this automatically.
    """
    return {"status": "ok", "message": "Resume Screener API is running"}


@router.post("/screen/text", response_model=ResumeScreenResponse)
def screen_from_text(request: ResumeScreenRequest):
    """
    Accepts resume and job description as plain text.
    Returns match score, matched skills, and missing skills.
    """
    try:
        result = screen_resume(request.resume_text, request.job_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/screen/pdf", response_model=ResumeScreenResponse)
async def screen_from_pdf(
    file: UploadFile = File(...),
    job_text: str = ""
):
    """
    Accepts resume as a PDF file upload and job description as text.
    Extracts text from PDF then runs the screening.
    """
    # make sure the uploaded file is actually a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    try:
        # read the PDF file as raw bytes
        file_bytes = await file.read()

        # extract text from the PDF
        resume_text = extract_text_from_pdf(file_bytes)

        # check if PDF had any readable text
        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. Make sure it is not a scanned image."
            )

        result = screen_resume(resume_text, job_text)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
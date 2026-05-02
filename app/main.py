# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# create the FastAPI app object
app = FastAPI(
    title="Resume Screener API",
    description="An NLP-powered API that matches resumes to job descriptions",
    version="1.0.0"
)

# allow requests from any frontend or tool (like Postman or a website)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# register the routes
app.include_router(router)
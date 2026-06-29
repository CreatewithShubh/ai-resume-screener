# main.py - The heart of our web server
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from parser import extract_text_from_pdf
from preprocessor import preprocess_text
from matcher import score_resumes

# Create the FastAPI app
app = FastAPI(title="AI Resume Screener")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def home():
    return {"message": "AI Resume Screener API is running!"}

# Main route - full AI pipeline
@app.post("/screen")
async def screen_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    # Step 1: Clean the job description
    cleaned_job_desc = preprocess_text(job_description)

    # Step 2: Process each resume
    processed_resumes = []
    for resume in resumes:
        file_bytes = await resume.read()
        raw_text = extract_text_from_pdf(file_bytes)
        cleaned_text = preprocess_text(raw_text)
        processed_resumes.append({
            "filename": resume.filename,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text
        })

    # Step 3: Score all resumes against job description
    results = score_resumes(cleaned_job_desc, processed_resumes)

    return {
        "message": "Screening complete!",
        "total_resumes": len(results),
        "results": results
    }
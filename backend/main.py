# main.py - The heart of our web server
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from parser import extract_text_from_pdf
from preprocessor import preprocess_text

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

# Upload route - receives resumes + job description
@app.post("/screen")
async def screen_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    # Step 1: Clean the job description
    cleaned_job_desc = preprocess_text(job_description)

    results = []

    for resume in resumes:
        # Step 2: Read the PDF
        file_bytes = await resume.read()
        
        # Step 3: Extract text from PDF
        raw_text = extract_text_from_pdf(file_bytes)
        
        # Step 4: Clean the resume text
        cleaned_text = preprocess_text(raw_text)

        results.append({
            "filename": resume.filename,
            "raw_preview": raw_text[:200],        # Original text
            "cleaned_preview": cleaned_text[:200]  # Cleaned text
        })

    return {
        "message": "Resumes preprocessed successfully!",
        "cleaned_job_description": cleaned_job_desc,
        "resumes": results
    }
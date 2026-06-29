# main.py - The heart of our web server
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from parser import extract_text_from_pdf

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
    results = []

    for resume in resumes:
        # Read the PDF file bytes
        file_bytes = await resume.read()
        
        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file_bytes)
        
        results.append({
            "filename": resume.filename,
            "text_length": len(extracted_text),
            "preview": extracted_text[:300]  # First 300 characters
        })

    return {
        "message": "Resumes parsed successfully!",
        "job_description_length": len(job_description),
        "resumes": results
    }
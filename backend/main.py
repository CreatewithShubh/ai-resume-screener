# main.py - The heart of our web server
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

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
    job_description: str = Form(...),       # Job description text
    resumes: List[UploadFile] = File(...)   # Multiple PDF files
):
    # For now just return the filenames to test it works
    filenames = [resume.filename for resume in resumes]
    return {
        "message": "Files received successfully!",
        "job_description_length": len(job_description),
        "resumes_received": filenames
    }
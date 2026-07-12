# main.py - The heart of our web server
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from parser import extract_text_from_pdf
from preprocessor import preprocess_text
from matcher import score_resumes
from summarizer import summarize_resume
import nltk

# Download NLTK data automatically on server startup
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Create the FastAPI app
app = FastAPI(title="AI Resume Screener")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
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
    try:
        # Step 1: Clean the job description
        cleaned_job_desc = preprocess_text(job_description)

        # Step 2: Process each resume
        processed_resumes = []
        for resume in resumes:
            try:
                file_bytes = await resume.read()
                raw_text = extract_text_from_pdf(file_bytes)
                cleaned_text = preprocess_text(raw_text)
                try:
                    summary = summarize_resume(raw_text)
                except:
                    summary = "Summary not available."
                processed_resumes.append({
                    "filename": resume.filename,
                    "raw_text": raw_text,
                    "cleaned_text": cleaned_text,
                    "summary": summary
                })
            except Exception as e:
                processed_resumes.append({
                    "filename": resume.filename,
                    "raw_text": "Could not read file.",
                    "cleaned_text": "",
                    "summary": "Could not process file."
                })

        # Step 3: Score all resumes
        results = score_resumes(cleaned_job_desc, processed_resumes)

        return {
            "message": "Screening complete!",
            "total_resumes": len(results),
            "results": results
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {
            "message": f"Error: {str(e)}",
            "total_resumes": 0,
            "results": []
        }
# matcher.py - The AI brain that scores resumes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_resumes(job_description: str, resumes: list) -> list:
    """
    Compares each resume against the job description.
    Returns a score from 0 to 100 for each resume.
    
    job_description: cleaned job description text
    resumes: list of dicts with 'filename' and 'cleaned_text'
    """
    # Combine job description with all resumes into one list
    # The job description always goes first (index 0)
    all_texts = [job_description] + [r['cleaned_text'] for r in resumes]
    
    # Step 1: Convert all texts to TF-IDF vectors (numbers)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Step 2: Calculate similarity between job description and each resume
    # tfidf_matrix[0] = job description vector
    # tfidf_matrix[1:] = resume vectors
    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(job_vector, resume_vectors)[0]
    
    # Step 3: Build results with scores
    results = []
    for i, resume in enumerate(resumes):
        score = round(float(similarities[i]) * 100, 2)  # Convert to percentage
        results.append({
            "filename": resume['filename'],
            "score": score,
            "raw_preview": resume['raw_text'][:200]
        })
    
    # Step 4: Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results
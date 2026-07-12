# matcher.py - The AI brain that scores resumes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A list of common skills we'll look for in resumes and job descriptions
COMMON_SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "nosql", "mongodb",
    "react", "angular", "vue", "node", "express", "django", "flask", "fastapi",
    "machine learning", "deep learning", "nlp", "data science", "pandas",
    "numpy", "scikit learn", "tensorflow", "pytorch", "keras",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "html", "css", "rest api", "graphql", "agile", "scrum",
    "excel", "tableau", "power bi", "data analysis", "data visualization",
    "communication", "leadership", "teamwork", "problem solving"
]

def find_skills(text: str) -> list:
    """
    Checks which skills from our list appear in the given text.
    """
    found = []
    for skill in COMMON_SKILLS:
        skill_cleaned = skill.replace(" ", "")
        text_cleaned = text.replace(" ", "")
        if skill_cleaned in text_cleaned:
            found.append(skill)
    return found

def score_resumes(job_description: str, resumes: list) -> list:
    """
    Compares each resume against the job description.
    Returns a score from 0 to 100, plus matched/missing skills.
    """
    all_texts = [job_description] + [r['cleaned_text'] for r in resumes]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(job_vector, resume_vectors)[0]

    # Find skills mentioned in the job description
    job_skills = set(find_skills(job_description))

    results = []
    for i, resume in enumerate(resumes):
        # Find skills in this resume FIRST
        resume_skills = set(find_skills(resume['cleaned_text']))

        # Base TF-IDF score
        base_score = float(similarities[i]) * 100

        # Skill match boost — more matched skills = higher score
        skill_boost = len(job_skills & resume_skills) * 5

        # Final score capped at 100
        score = round(min(base_score + skill_boost, 100), 2)

        # Matched = skills in BOTH job description and resume
        matched_skills = list(job_skills & resume_skills)

        # Missing = skills in job description but NOT in resume
        missing_skills = list(job_skills - resume_skills)

        results.append({
            "filename": resume['filename'],
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "raw_preview": resume['raw_text'][:200],
            "summary": resume.get('summary', 'No summary available.')
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results
# summarizer.py - Generates a short summary of each resume
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def summarize_resume(raw_text: str, num_sentences: int = 3) -> str:
    """
    Extracts the most important sentences from a resume.
    Think of it like finding the highlights of a document.
    
    raw_text: original resume text
    num_sentences: how many sentences to include in summary
    """
    # Split text into sentences
    sentences = [s.strip() for s in raw_text.replace('\n', ' ').split('.') if len(s.strip()) > 20]
    
    if len(sentences) == 0:
        return "No summary available."
    
    if len(sentences) <= num_sentences:
        return '. '.join(sentences[:num_sentences]) + '.'
    
    # Use TF-IDF to find most important sentences
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform(sentences)
        # Score each sentence by sum of its TF-IDF values
        scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        # Get top sentences
        top_indices = scores.argsort()[-num_sentences:][::-1]
        top_indices = sorted(top_indices)  # Keep original order
        summary = '. '.join([sentences[i] for i in top_indices]) + '.'
        return summary
    except:
        return '. '.join(sentences[:num_sentences]) + '.'
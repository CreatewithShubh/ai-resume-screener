# preprocessor.py - Cleans and prepares text for the AI
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import nltk

# Tell NLTK where to save data on the server
nltk.data.path.append('/opt/render/project/src/nltk_data')

# Download required data
nltk.download('punkt', download_dir='/opt/render/project/src/nltk_data')
nltk.download('stopwords', download_dir='/opt/render/project/src/nltk_data')
nltk.download('wordnet', download_dir='/opt/render/project/src/nltk_data')
nltk.download('punkt_tab', download_dir='/opt/render/project/src/nltk_data')

# Load the lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    """
    Cleans raw text in 5 steps:
    1. Lowercase everything
    2. Remove punctuation and special characters
    3. Tokenize (split into words)
    4. Remove stop words
    5. Lemmatize (reduce words to base form)
    """
    # Step 1: Lowercase
    text = text.lower()
    
    # Step 2: Remove punctuation and special characters
    # Keep only letters, numbers and spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Step 3: Tokenize - split into individual words
    tokens = word_tokenize(text)
    
    # Step 4 & 5: Remove stop words and lemmatize
    cleaned_tokens = []
    for token in tokens:
        # Skip stop words and very short words
        if token not in stop_words and len(token) > 2:
            # Lemmatize - convert to base form
            lemma = lemmatizer.lemmatize(token)
            cleaned_tokens.append(lemma)
    
    # Join back into a single string
    return ' '.join(cleaned_tokens)

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import string
import re

print("Starting model training process...")

# --- Download NLTK data (if not already downloaded) ---
print("Downloading NLTK assets...")
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
print("NLTK assets are ready.")

# --- 1. Load Data ---
print("Loading dataset...")
try:
    df = pd.read_csv("fake_job_postings.csv")
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("\n[ERROR] `fake_job_postings.csv` not found.")
    print("Please download the dataset from https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction")
    print("And place it in the same folder as this script.")
    exit()

# --- 2. Preprocessing ---
print("Preprocessing data...")
# Fill missing values
df = df.fillna('')

# Combine relevant text fields into one
df['combined_text'] = df['title'] + ' ' + df['company_profile'] + ' ' + df['description'] + ' ' + df['requirements'] + ' ' + df['benefits']

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """Cleans and preprocesses text."""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove stopwords and lemmatize
    words = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return ' '.join(words)

df['processed_text'] = df['combined_text'].apply(preprocess_text)
print("Data preprocessing complete.")

# --- 3. TF-IDF Vectorization ---
print("Applying TF-IDF Vectorizer...")
tfidf_vectorizer = TfidfVectorizer(max_features=7000) # Using more features for better accuracy
X = tfidf_vectorizer.fit_transform(df['processed_text'])
y = df['fraudulent']
print("Vectorization complete.")

# --- 4. Model Training ---
print("Training Logistic Regression model...")
model = LogisticRegression(solver='liblinear', C=1.0, random_state=42)
model.fit(X, y)
print("Model training complete.")

# --- 5. Save the Model and Vectorizer ---
print("Saving model and vectorizer to disk...")
joblib.dump(model, 'fake_job_model.joblib')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')

print("\n✅ Success! The model and vectorizer have been saved.")
print("You can now run the `app.py` file to launch the web application.")
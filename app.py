import streamlit as st
import joblib
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import time
import requests
from streamlit_lottie import st_lottie

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Job Authenticity Checker",
    page_icon="✨",
    layout="centered",
)

# --- LOAD LOCAL CSS FOR STYLING ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- ASSET LOADERS (CACHED) ---
@st.cache_resource
def load_ml_assets():
    if not os.path.exists('fake_job_model.joblib') or not os.path.exists('tfidf_vectorizer.joblib'):
        st.error("🚨 Model files not found! Please run `train.py` first.")
        st.stop()
    model = joblib.load('fake_job_model.joblib')
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    return model, vectorizer

@st.cache_data
def load_lottie_animation(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.cache_resource
def download_nltk_data():
    nltk_data = ['stopwords', 'wordnet']
    for item in nltk_data:
        try: nltk.data.find(f'corpora/{item}')
        except LookupError: nltk.download(item)

# --- LOAD ASSETS ---
model, tfidf_vectorizer = load_ml_assets()
download_nltk_data()
lottie_header = load_lottie_animation("https://assets1.lottiefiles.com/packages/lf20_s2lryxtd.json")
lottie_success = load_lottie_animation("https://assets1.lottiefiles.com/packages/lf20_z4hbaa36.json")
lottie_warning = load_lottie_animation("https://assets7.lottiefiles.com/packages/lf20_Tkwjw8.json")

# --- TEXT PREPROCESSING FUNCTION ---
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
def preprocess_text(text):
    if not isinstance(text, str): return ""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return ' '.join(words)

# --- INITIALIZE SESSION STATE ---
if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.inputs = {}

# --- HEADER ---
if lottie_header:
    st_lottie(lottie_header, height=200, speed=1, key="header")

st.title("Job Authenticity Checker")
st.markdown("Move forward in your career with confidence. Paste a job posting below, and our AI will instantly analyze it for signs of fraud.")
st.divider()

# --- INPUT FORM ---
with st.form("job_input_form"):
    st.markdown("### Job Details")
    job_title = st.text_input("Job Title", st.session_state.inputs.get("job_title", ""))
    company_name = st.text_input("Company Name", st.session_state.inputs.get("company_name", ""))
    description = st.text_area("Job Description & Requirements", st.session_state.inputs.get("description", ""), height=200)

    submitted = st.form_submit_button("Verify Authenticity")

if submitted:
    st.session_state.inputs = {"job_title": job_title, "company_name": company_name, "description": description}
    combined_text = ' '.join(st.session_state.inputs.values())

    if not combined_text.strip():
        st.warning("Please provide some details about the job posting.")
    else:
        with st.spinner("Engaging AI analysis protocols..."):
            processed_text = preprocess_text(combined_text)
            text_vector = tfidf_vectorizer.transform([processed_text])
            prediction = model.predict(text_vector)[0]
            confidence = model.predict_proba(text_vector).max()
            time.sleep(1.5) # Simulate processing for a better experience
        st.session_state.result = {"prediction": prediction, "confidence": confidence}

# --- DISPLAY RESULT ---
if st.session_state.result:
    result = st.session_state.result
    pred = result["prediction"]
    conf = result["confidence"]
    
    if pred == 0:
        result_class, title, message, lottie_anim = "real", "Authentic", "This post looks legitimate. Good luck with your application!", lottie_success
    else:
        result_class, title, message, lottie_anim = "warning", "Potentially Fake", "This post has traits of fraudulent listings. Please proceed with caution.", lottie_warning
    
    # --- Result Card ---
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Card Header
    st.markdown(f'<div class="result-card-header {result_class}"><h2 class="result-title">{title}</h2></div>', unsafe_allow_html=True)
    
    # Card Body
    st.markdown('<div class="result-body">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        if lottie_anim:
            st_lottie(lottie_anim, height=120, speed=1, loop=False, key="result_anim")
    with col2:
        st.markdown(f"**{message}**")
        st.markdown(f"Our model is **{conf:.2%}** confident in this result.")
        st.progress(conf, text="")

    st.markdown('</div></div>', unsafe_allow_html=True)
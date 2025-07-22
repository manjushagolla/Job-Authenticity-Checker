
# 🛡️✨ Job Authenticity Checker

An intelligent web application built with Python and Streamlit that uses Natural Language Processing (NLP) to detect fraudulent job postings. This tool provides a layer of security for job seekers by analyzing job details and flagging potentially fake listings.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://job-appenticity-checker-autgyp2vxbxgmng8mmc3my.streamlit.app/)


---

## ✨ Features

- **Intuitive & Clean UI:** A minimalist and user-centric interface designed for ease of use.
- **Organized Input Sections:** Details are neatly organized into expandable sections (Job Title, Description, etc.).
- **Real-Time AI Analysis:** Uses a pre-trained Logistic Regression model to provide instant predictions.
- **Dynamic & Animated Results:** The verdict is displayed in a vibrant, animated card that is both informative and engaging.
- **Confidence Score:** Visually represents the model's confidence in its prediction.
- **Fully Responsive:** Looks and works great on both desktop and mobile devices.

---

## 🛠️ Tech Stack

- **Backend & ML:** Python
- **Machine Learning:** Scikit-learn
- **NLP:** NLTK (Natural Language Toolkit)
- **Web Framework:** Streamlit
- **Data Manipulation:** Pandas
- **Animations:** Lottie for Streamlit

---

## 🚀 How to Run Locally

### Prerequisites

- Python 3.8+
- `pip` package manager
- A virtual environment tool like `venv` (recommended)

### 1. Clone the Repository


git clone https://github.com/manjushagolla/Job-Authenticity-Checker.git <br>
cd Job-Authenticity-Checker


### 2. Set Up a Virtual Environment
**Create virtual environment**
python -m venv venv

**Activate it
On Windows:**
venv\Scripts\activate
**On macOS/Linux:**
source venv/bin/activate
## 3. Install Dependencies

pip install -r requirements.txt

## 4. Train the Model (One-Time Step)
**a. Download the Dataset:**
Get the dataset from Kaggle: <br>
- Fake Job Postings Dataset

- Place fake_job_postings.csv in the root folder.

**b. Run the Training Script:**

python train.py <br>
This will create:

- fake_job_model.joblib

- tfidf_vectorizer.joblib

## 5. Run the Streamlit App


streamlit run app.py <br>
Then open http://localhost:8501 in your browser.


---

## Files Required for Deployment:
- app.py

- requirements.txt

- fake_job_model.joblib

- tfidf_vectorizer.joblib

- style.css (optional)

- Streamlit Cloud automatically deploys the app on every push to the main branch.

---

## 📈 Model Overview
- Trained on 17,000+ job postings (real & fake)

- Preprocessing: Lowercasing, stopword removal, punctuation removal

- Lemmatization with nltk

- Vectorization with TF-IDF

- Classification using Logistic Regression

---

## **🙏 Acknowledgements**
-**Dataset:** Fake Job Postings Prediction Dataset by Shivam Bansal

-**Framework:** Streamlit

-**Animations:** LottieFiles













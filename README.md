# 🚨 Fake Instagram Account Detector

A machine learning-powered app that detects whether a given Instagram account is **genuine** or **fake**, using features publicly available from user profiles.

---

## 📦 Project Overview

- 🔍 **Purpose**: Identify fake/spammy Instagram accounts using ML.
- 🤖 **Model**: Random Forest Classifier.
- 📊 **Training Dataset**: `sample_data.csv` (custom, curated dataset).
- 🛠 **Tech Stack**:
  - Python, Scikit-learn, Flask
  - React.js frontend
  - Instaloader for Instagram scraping

---

## 🧠 ML Model Details

- **Classifier**: Random Forest
- **Input Features**:
  - `num_followers`
  - `num_following`
  - `num_posts`
  - `has_profile_picture`
  - `bio_length`
  - `is_verified`
- **Output**: Binary prediction — `FAKE` or `REAL`
- **Training Accuracy**: ~100% (on small sample dataset)

---

## 📁 File Structure

Fake-Instagram-Account-Detector/ ├── app.py # Flask backend ├── sample_data.csv # Training dataset ├── train_model.ipynb # Jupyter notebook for training ├── fake_instagram_account_model.pkl # Trained model ├── frontend/ # React frontend ├── archive/ # Legacy scripts & samples │ └── instagram_fake_accounts_sample.csv ├── README.md

yaml
Copy
Edit

---

## 🚀 How to Run the Project

### 🔧 Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
🌐 Frontend (React)
bash
Copy
Edit
cd frontend
npm install
npm start
App runs at: http://localhost:3000
API runs at: http://localhost:5000/predict?username=example#   F a k e - I n s t a g r a m - A c c o u n t - D e t e c t o r  
 
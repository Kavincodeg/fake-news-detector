# 📰 AI Fake News Detector

An AI-powered system that detects whether a news article is **Real or Fake** using Natural Language Processing (NLP), Machine Learning, and Web Scraping.

---

## 🚀 Features

- 🔗 Analyze news directly from URL
- 🧠 Fake vs Real prediction using ML model
- 🌐 Source credibility scoring
- 📊 Final trust score calculation
- 🧾 Keyword-based explanation
- 📰 Extract article content from websites
- ⚠️ Handles protected/blocked sites (Cloudflare-aware)
- 📈 Interactive Streamlit dashboard

---

## 🛠️ Tech Stack

- **Python**
- **Scikit-learn (Logistic Regression, TF-IDF)**
- **Streamlit** (Frontend)
- **Trafilatura + BeautifulSoup + Selenium** (Web Scraping)
- **Pandas, NumPy**

---

## 📊 Model Performance

- ✅ Accuracy: **~98%**
- Model: Logistic Regression
- Vectorization: TF-IDF

---

## 🧠 How It Works

1. User enters a **news URL**
2. System extracts article text using hybrid scraping:
   - Trafilatura (primary)
   - BeautifulSoup (fallback)
   - Selenium (for protected sites)
3. Text is cleaned and processed
4. ML model predicts:
   - **Real ✅**
   - **Fake ❌**
5. Source credibility is evaluated
6. Final trust score is displayed

---

## ▶️ Run Locally

### 1. Clone repository
```bash
git clone https://github.com/Kavincodeg/fake-news-detector.git
cd fake-news-detector

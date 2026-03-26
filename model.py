import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Train model dynamically (small version for deployment)
data = pd.read_csv("data/news.csv")

X = data['text']
y = data['label']

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vectorized, y)


def predict_news(text):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    prob = model.predict_proba(vector)[0]

    confidence = max(prob)

    if prediction == 0:
        return "Real ✅", confidence
    else:
        return "Fake ❌", confidence


def get_top_words(text):
    words = text.split()
    return words[:10]
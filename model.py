import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_news(text):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    prob = model.predict_proba(vector)[0]

    confidence = max(prob)

    if prediction == 0:
        return "Real ✅", confidence
    else:
        return "Fake ❌", confidence


# 🧠 Explanation feature (NEW)
def get_top_words(text):
    words = text.split()
    return words[:10]
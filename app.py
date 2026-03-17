import streamlit as st
import pandas as pd
from model import predict_news, get_top_words
from utils import (
    extract_text_from_url,
    clean_text,
    get_source_credibility,
    detect_url_type
)

# Page config
st.set_page_config(page_title="AI Fake News Detector", layout="centered")

# Title
st.title("📰 AI Fake News Detector")
st.write("Analyze news articles using URL and detect whether they are Real or Fake.")

# Input URL
url = st.text_input("🔗 Enter News URL")

# Analyze button
if st.button("Analyze"):
    if url.strip() != "":

        # Detect URL type
        url_type = detect_url_type(url)

        if url_type != "news":
            st.warning("⚠️ This project currently supports only news article URLs.")
            st.stop()

        # Extract article text
        text = extract_text_from_url(url)

        # ❗ IMPORTANT FIX (Cloudflare / blocked sites)
        if not text:
            st.error("❌ Unable to extract article. This site may be protected (Cloudflare) or unsupported.")
            st.stop()

        # Clean text
        cleaned = clean_text(text)

        # Prediction
        label, confidence = predict_news(cleaned)

        # Source credibility
        credibility_label, credibility_score = get_source_credibility(url)

        # Final score
        final_score = (confidence + credibility_score) / 2

        # ---------------- RESULT ----------------
        st.subheader("📊 Analysis Result")

        if "Fake" in label:
            st.error(f"🚨 Prediction: {label}")
        else:
            st.success(f"✅ Prediction: {label}")

        st.write(f"🧠 Model Confidence: {confidence:.2f}")
        st.write(f"🌐 Source Credibility: {credibility_label} ({credibility_score})")

        # Final trust score
        if final_score > 0.7:
            st.success(f"✅ Final Trust Score: {final_score:.2f} (Reliable)")
        else:
            st.warning(f"⚠️ Final Trust Score: {final_score:.2f} (Suspicious)")

        # ---------------- EXPLANATION ----------------
        st.subheader("🧾 Key Words (Explanation)")
        st.write(get_top_words(cleaned))

        # ---------------- ARTICLE TEXT ----------------
        with st.expander("📝 Extracted Article Text"):
            st.write(text[:1500])

    else:
        st.warning("⚠️ Please enter a URL")

# ---------------- DATASET DASHBOARD ----------------
st.markdown("---")
st.subheader("📊 Dataset Insights")

if st.checkbox("Show Dataset Analysis"):
    data = pd.read_csv("data/news.csv")

    st.write("### Label Distribution")
    st.bar_chart(data['label'].value_counts())

    st.write("### Sample Data")
    st.dataframe(data.sample(5))

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Built using Machine Learning + NLP + Streamlit")
st.caption("⚠️ Note: Some websites may block automated extraction due to security protections like Cloudflare.")
import trafilatura
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# Selenium (for difficult/protected sites)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


# 🚫 Detect blocked/invalid content (Cloudflare etc.)
def is_blocked_content(text):
    if not text:
        return True

    blocked_keywords = [
        "cloudflare",
        "attention required",
        "security service",
        "blocked",
        "verify you are human",
        "enable javascript"
    ]

    text_lower = text.lower()

    for word in blocked_keywords:
        if word in text_lower:
            return True

    return False


# 🔗 MAIN extraction function
def extract_text_from_url(url):

    # 1️⃣ Try trafilatura (best for most sites)
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)

        if text and len(text) > 300 and not is_blocked_content(text):
            return text

    except Exception as e:
        print("Trafilatura error:", e)

    # 2️⃣ Try requests + BeautifulSoup
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

        res = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        if text and len(text) > 300 and not is_blocked_content(text):
            return text

    except Exception as e:
        print("BeautifulSoup error:", e)

    # 3️⃣ Selenium fallback (for Cloudflare-like sites)
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get(url)
        time.sleep(5)

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        text = " ".join([p.text for p in paragraphs])

        driver.quit()

        if text and len(text) > 300 and not is_blocked_content(text):
            return text

    except Exception as e:
        print("Selenium error:", e)

    # ❌ Final fallback (failed extraction)
    return None


# 🧹 Clean text
def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# 🌐 Extract domain safely
def get_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ""


# ⭐ Source credibility scoring
def get_source_credibility(url):
    trusted_sources = [
        "bbc.com",
        "reuters.com",
        "thehindu.com",
        "ndtv.com",
        "timesofindia.indiatimes.com"
    ]

    domain = get_domain(url)

    for source in trusted_sources:
        if source in domain:
            return "High ✅", 0.9

    return "Low ⚠️", 0.4


# 🔍 Detect URL type
def detect_url_type(url):
    if "instagram.com" in url:
        return "instagram"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "twitter.com" in url or "x.com" in url:
        return "twitter"
    elif "facebook.com" in url:
        return "facebook"
    else:
        return "news"
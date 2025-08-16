import requests
import streamlit as st
from datetime import datetime

# ---------------------------
API_KEY = "4c62a75721f74a4a9dd169e202489b63"  
BASE_URL = "https://newsapi.org/v2/top-headlines"
# ---------------------------
def get_news(country="us", category=None, query=None):
    """Fetch latest news from NewsAPI with filters."""
    params = {
        "apiKey": API_KEY,
        "country": country,
        "pageSize": 20,   # max articles per page
    }
    if category and category != "All":
        params["category"] = category
    if query:
        params["q"] = query

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") == "ok":
        return data.get("articles", [])
    else:
        return []


st.set_page_config(page_title="📰 News Dashboard", page_icon="🗞️", layout="wide")

# Title
st.title("📰 Live News Dashboard")
st.markdown("### Get the latest headlines with filters")

# Sidebar Filters
st.sidebar.header("🔍 Filter News")
country = st.sidebar.selectbox("🌍 Country", ["us", "in", "gb", "au", "ca"])
category = st.sidebar.selectbox(
    "📂 Category",
    ["All", "business", "entertainment", "general", "health", "science", "sports", "technology"]
)
query = st.sidebar.text_input("🔎 Search by Keyword")

refresh = st.sidebar.button("🔄 Refresh News")

# Auto-load news on start / when refreshed
articles = get_news(country=country, category=category, query=query)

# ---------------------------
# DISPLAY NEWS
# ---------------------------
if not articles:
    st.warning("⚠️ No articles found. Try different filters.")
else:
    for article in articles:
        with st.container():
            st.markdown(f"### {article['title']}")
            if article.get("urlToImage"):
                st.image(article["urlToImage"], use_container_width=True)
            else:
                st.image("https://via.placeholder.com/600x300.png?text=No+Image+Available", use_container_width=True)
            st.write(article.get("description", "No description available."))

            # Source & Published Date
            source = article["source"]["name"]
            published_time = article.get("publishedAt", "")
            if published_time:
                published_time = datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%SZ")
                published_time = published_time.strftime("%d %b %Y, %I:%M %p")

            st.caption(f"📰 {source} | 📅 {published_time}")
            st.markdown(f"[👉 Read Full Article]({article['url']})")
            st.markdown("---")  ṣ

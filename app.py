import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import random

# Page Config
st.set_page_config(page_title="AI Job Finder", page_icon="💼")

# Motivational Quotes
quotes = [
    "🌟 The best way to predict the future is to create it.",
    "💡 Opportunities don't happen, you create them.",
    "🚀 Dream big. Work hard. Make it happen."
]

# App Title
st.title("🚀 AI-Powered Job Finder")
st.sidebar.header("💡 Motivational Quote")
st.sidebar.write(random.choice(quotes))

# Sidebar Filters
st.sidebar.header("🎯 Find Your Dream Job")
job_category = st.sidebar.selectbox("Select Job Category", [
    "Next.js Developer", "Python Developer", "Graphic Designer", "Frontend Intern", 
    "Backend Intern", "Junior Frontend Developer", "Senior Backend Developer"
])
location = st.sidebar.selectbox("Preferred Location", [
    "Remote", "USA", "Canada", "UK", "Germany", "India", "Pakistan"
])

# Function to Scrape Jobs from LinkedIn
def fetch_jobs_from_linkedin(job_category, location):
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_category.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return pd.DataFrame(columns=["Job Title", "Company", "Location", "Apply Link"])

    soup = BeautifulSoup(response.text, "html.parser")
    job_listings = []

    for job in soup.find_all("div", class_="base-search-card__info"):
        title = job.find("h3")
        company = job.find("h4")
        link_tag = job.find("a")
        link = link_tag["href"] if link_tag else ""

        if title and company and link and "*****" not in title.text.strip():
            job_listings.append([title.text.strip(), company.text.strip(), location, link])

    return pd.DataFrame(job_listings, columns=["Job Title", "Company", "Location", "Apply Link"])

# Fetch Jobs
df = fetch_jobs_from_linkedin(job_category, location)

# **Filter Valid Jobs (Jahan Data Properly Maujood Ho)**
df = df.dropna(subset=["Job Title", "Company", "Apply Link"])

# Show Jobs
st.subheader("📋 Available Jobs")
if df.empty:
    st.warning("❌ Sorry! No jobs found for your selected category and location.")
else:
    for index, row in df.iterrows():
        with st.container():
            st.write(f"### {row['Job Title']} - {row['Company']}")
            st.write(f"📍 **Location:** {row['Location']}")
            st.markdown(f"[📝 Apply Now]({row['Apply Link']})", unsafe_allow_html=True)
            st.markdown("---")

# Show Job Trends
st.subheader("📊 Job Market Trends")
if not df.empty:
    fig = px.bar(df, x="Company", title="Company-wise Job Openings", color="Company")
    st.plotly_chart(fig)

# Footer
st.markdown("🛠 **Developed by Warisha Akram** | 🚀 **AI-Powered Job Search App**")


import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Recruiter Agent", layout="wide")

st.title("🤖 AI Recruiter Agent")
st.write("Paste a Job Description and get ranked candidates instantly.")

candidates = [
    {"name":"Asha Raman","title":"Power BI Developer","experience":4,"skills":["sql","power bi","dax","python"],"location":"Chennai","notice_days":30},
    {"name":"Kiran S","title":"Data Analyst","experience":3,"skills":["sql","power bi","power query","excel"],"location":"Bangalore","notice_days":15},
    {"name":"Meera V","title":"BI Analyst","experience":5,"skills":["excel","tableau","sql"],"location":"Chennai","notice_days":60},
]

jd = st.text_area(
    "Job Description",
    height=220,
    value="We are hiring a Power BI Developer with 3+ years experience. Must have SQL, DAX, Power Query, Power BI Service. Preferred: Python, Azure. Location: Chennai / Hybrid."
)

def rank_candidates(jd_text):
    jd_lower = jd_text.lower()
    results = []

    for c in candidates:
        overlap = sum(1 for s in c["skills"] if s in jd_lower)
        skill_score = min(40, overlap * 10)
        exp_score = min(25, c["experience"] * 5)
        title_score = 20 if any(x in c["title"].lower() for x in ["analyst","developer","engineer"]) else 10
        location_score = 15 if c["location"].lower() == "chennai" else 8

        match_score = skill_score + exp_score + title_score + location_score
        interest_score = 90 if c["notice_days"] <= 30 else 65
        final_score = round(match_score * 0.7 + interest_score * 0.3, 2)

        results.append({
            "name": c["name"],
            "title": c["title"],
            "match_score": match_score,
            "interest_score": interest_score,
            "final_score": final_score,
            "why": f"Matched {overlap} skills, {c['experience']} years experience, notice {c['notice_days']} days"
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)

if st.button("Find Candidates"):
    df = pd.DataFrame(rank_candidates(jd))
    st.dataframe(df, use_container_width=True)

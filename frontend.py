import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="AI Recruiter Agent V2.1", layout="wide")

# -------------------------
# Load Candidates from CSV
# -------------------------
@st.cache_data
def load_candidates():
    df = pd.read_csv("candidates.csv")

    # Convert skills string -> list
    df["skills"] = df["skills"].fillna("").apply(
        lambda x: [i.strip().lower() for i in str(x).split(",")]
    )

    return df.to_dict(orient="records")

candidates = load_candidates()

known_skills = [
    "sql", "python", "power bi", "dax",
    "power query", "excel", "azure", "tableau"
]

# -------------------------
# JD Parsing
# -------------------------
def parse_jd(jd):
    text = jd.lower()

    found_skills = [s for s in known_skills if s in text]

    exp_match = re.search(r'(\d+)\+?\s*years?', text)
    experience = int(exp_match.group(1)) if exp_match else "Not specified"

    location = "Chennai" if "chennai" in text else (
        "Bangalore" if "bangalore" in text else "Not specified"
    )

    role = "Power BI Developer" if "power bi developer" in text else (
        "Data Analyst" if "data analyst" in text else "Not specified"
    )

    return {
        "role": role,
        "skills": found_skills,
        "experience": experience,
        "location": location
    }

# -------------------------
# Scoring Engine
# -------------------------
def rank_candidates(parsed):
    results = []

    for c in candidates:
        overlap = sum(1 for s in c["skills"] if s in parsed["skills"])
        missing = [s for s in parsed["skills"] if s not in c["skills"]]

        # Match Score
        skill_score = min(40, overlap * 10)
        exp_score = min(25, int(c["experience"]) * 5)

        title_score = 20 if any(
            x in str(c["title"]).lower()
            for x in ["analyst", "developer", "engineer"]
        ) else 10

        location_score = (
            15 if str(parsed["location"]).lower() == str(c["location"]).lower()
            else 8
        )

        match_score = skill_score + exp_score + title_score + location_score

        # Simulated Outreach
        notice = int(c["notice_days"])

        candidate_reply = (
            f"Yes, I’m interested. Available in {notice} days."
            if notice <= 30
            else f"Interested, but available in {notice} days."
        )

        interest_score = 90 if notice <= 30 else 65

        final_score = round((match_score * 0.7) + (interest_score * 0.3), 2)

        why = (
            f"{overlap} skill match, "
            f"{c['experience']} yrs exp, "
            f"located in {c['location']}"
        )

        results.append({
            "name": c["name"],
            "title": c["title"],
            "match_score": match_score,
            "interest_score": interest_score,
            "final_score": final_score,
            "why_matched": why,
            "missing_skills": ", ".join(missing) if missing else "None",
            "agent_msg": (
                f"Hi {c['name']}, we found a {parsed['role']} "
                f"role in {parsed['location']}. Interested?"
            ),
            "candidate_reply": candidate_reply
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)

# -------------------------
# UI
# -------------------------
st.title("🤖 AI Recruiter Agent (CSV Version)")
st.write("JD Parsing • Candidate Discovery • Simulated Outreach • Ranked Shortlist")

jd = st.text_area(
    "Paste Job Description",
    height=220,
    value="""We are hiring a Power BI Developer with 3+ years experience.
Must have SQL, DAX, Power Query, Power BI Service.
Preferred: Python, Azure.
Location: Chennai / Hybrid."""
)

if st.button("Find Candidates"):
    parsed = parse_jd(jd)

    # JD Parsing Panel
    st.subheader("📌 Parsed Job Description")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Role", parsed["role"])
    col2.metric("Experience", parsed["experience"])
    col3.metric("Location", parsed["location"])
    col4.metric("Skills Found", len(parsed["skills"]))

    st.write("**Required Skills:**", ", ".join(parsed["skills"]))

    # Candidate Results
    results = rank_candidates(parsed)

    st.subheader("🔍 Candidate Discovery & Matching")

    match_df = pd.DataFrame([
        {
            "Name": r["name"],
            "Title": r["title"],
            "Match Score": r["match_score"],
            "Why Matched": r["why_matched"],
            "Missing Skills": r["missing_skills"]
        }
        for r in results
    ])

    st.dataframe(match_df, use_container_width=True)

    # Simulated Outreach
    st.subheader("💬 Simulated Conversational Outreach")

    for r in results[:10]:
        with st.expander(f"Conversation with {r['name']}"):
            st.write(f"**Agent:** {r['agent_msg']}")
            st.write(f"**Candidate:** {r['candidate_reply']}")
            st.write(f"**Interest Score:** {r['interest_score']}")

    # Final Shortlist
    st.subheader("🏆 Final Ranked Shortlist")

    final_df = pd.DataFrame([
        {
            "Rank": i + 1,
            "Candidate": r["name"],
            "Match Score": r["match_score"],
            "Interest Score": r["interest_score"],
            "Final Score": r["final_score"]
        }
        for i, r in enumerate(results[:20])
    ])

    st.dataframe(final_df, use_container_width=True)

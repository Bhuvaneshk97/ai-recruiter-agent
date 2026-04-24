import streamlit as st
import pandas as pd
import re

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Recruiter Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #eef2f7;
}
.section-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #eef2f7;
}
.small-muted {
    color:#64748b;
    font-size:14px;
}
.big-title {
    font-size:48px;
    font-weight:800;
    color:#4f46e5;
}
.sub-title {
    color:#475569;
    margin-top:-10px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Load CSV ----------------
@st.cache_data
def load_candidates():
    df = pd.read_csv("candidates.csv")
    df["skills"] = df["skills"].fillna("").apply(
        lambda x: [i.strip().lower() for i in str(x).split(",")]
    )
    return df

df_candidates = load_candidates()

known_skills = [
    "sql", "python", "power bi", "dax",
    "power query", "excel", "azure", "tableau"
]

# ---------------- Functions ----------------
def parse_jd(jd):
    text = jd.lower()

    found_skills = [s for s in known_skills if s in text]

    exp_match = re.search(r'(\d+)\+?\s*years?', text)
    experience = int(exp_match.group(1)) if exp_match else 0

    location = "Chennai" if "chennai" in text else (
        "Bangalore" if "bangalore" in text else "All"
    )

    role = "Power BI Developer" if "power bi" in text else (
        "Data Analyst" if "analyst" in text else "Open Role"
    )

    return {
        "role": role,
        "skills": found_skills,
        "experience": experience,
        "location": location
    }

def score_candidates(parsed):
    rows = []

    for _, c in df_candidates.iterrows():
        overlap = sum(1 for s in c["skills"] if s in parsed["skills"])
        missing = [s for s in parsed["skills"] if s not in c["skills"]]

        skill_score = min(40, overlap * 10)
        exp_score = min(25, int(c["experience"]) * 5)

        title_score = 20 if any(
            x in str(c["title"]).lower()
            for x in ["developer", "analyst", "engineer"]
        ) else 10

        location_score = 15 if (
            parsed["location"] == "All" or
            str(c["location"]).lower() == parsed["location"].lower()
        ) else 8

        match_score = skill_score + exp_score + title_score + location_score

        notice = int(c["notice_days"])
        interest_score = 90 if notice <= 30 else 65

        final_score = round(match_score * 0.7 + interest_score * 0.3, 2)

        rows.append({
            "name": c["name"],
            "title": c["title"],
            "experience": c["experience"],
            "location": c["location"],
            "match_score": match_score,
            "interest_score": interest_score,
            "final_score": final_score,
            "missing_skills": ", ".join(missing) if missing else "None"
        })

    return pd.DataFrame(rows).sort_values("final_score", ascending=False)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("🤖 AI Recruiter Agent")
    st.caption("AI-powered candidate discovery & ranking")

    st.markdown("---")
    st.subheader("📄 Job Description")

    jd = st.text_area(
        "Paste JD",
        height=220,
        value="""We are hiring a Power BI Developer with 3+ years experience.
Must have SQL, DAX, Power Query, Power BI Service.
Preferred: Python, Azure.
Location: Chennai / Hybrid."""
    )

    run_btn = st.button("🚀 Find Candidates", use_container_width=True)

    st.markdown("---")
    st.info("Built for hackathon demo • Recruit smarter, faster.")

# ---------------- Main Header ----------------
st.markdown('<div class="big-title">✨ AI Recruiter Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Automate candidate discovery, outreach and shortlisting using AI</div>',
    unsafe_allow_html=True
)

if run_btn:
    parsed = parse_jd(jd)
    result_df = score_candidates(parsed)

    # ---------------- Metrics ----------------
    top_score = result_df["final_score"].max()
    high_interest = (result_df["interest_score"] >= 90).sum()
    strong_matches = (result_df["match_score"] >= 80).sum()
    total = len(result_df)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="metric-card">👥 <b>Total Candidates</b><br><span class="big-number">'+str(total)+'</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card">✅ <b>Matches Found</b><br>{strong_matches}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card">⭐ <b>High Interest</b><br>{high_interest}</div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card">🏆 <b>Top Score</b><br>{top_score}</div>', unsafe_allow_html=True)

    st.write("")

    # ---------------- Tabs ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 JD Parsing",
        "🔍 Candidate Matches",
        "💬 Outreach",
        "🏆 Final Shortlist"
    ])

    # Tab 1
    with tab1:
        col1, col2 = st.columns([2,1])

        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Parsed Job Description")
            st.write(f"**Role:** {parsed['role']}")
            st.write(f"**Experience:** {parsed['experience']}+ years")
            st.write(f"**Location:** {parsed['location']}")
            st.write(f"**Skills:** {', '.join(parsed['skills'])}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("Skills Count")
            skills_df = pd.DataFrame({
                "Skill": parsed["skills"],
                "Count": [1]*len(parsed["skills"])
            })
            if len(skills_df) > 0:
                st.bar_chart(skills_df.set_index("Skill"))
            st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2
    with tab2:
        st.subheader("Top Matching Candidates")
        st.dataframe(
            result_df[[
                "name","title","experience","location",
                "match_score","interest_score","final_score","missing_skills"
            ]].head(20),
            use_container_width=True
        )

    # Tab 3
    with tab3:
        st.subheader("Simulated Conversational Outreach")
        for _, row in result_df.head(5).iterrows():
            with st.expander(f"Conversation with {row['name']}"):
                st.write(f"**Agent:** Hi {row['name']}, we found a {parsed['role']} role in {parsed['location']}. Interested?")
                if row["interest_score"] >= 90:
                    st.write("**Candidate:** Yes, I’m interested and available soon.")
                else:
                    st.write("**Candidate:** Interested, but my availability is later.")
                st.write(f"**Interest Score:** {row['interest_score']}")

    # Tab 4
    with tab4:
        st.subheader("Final Ranked Shortlist")

        shortlist = result_df.head(20).copy()
        shortlist.insert(0, "rank", range(1, len(shortlist)+1))

        st.dataframe(shortlist, use_container_width=True)

        csv = shortlist.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Shortlist (CSV)",
            csv,
            "shortlist.csv",
            "text/csv",
            use_container_width=True
        )
else:
    st.info("👈 Paste a Job Description in the sidebar and click **Find Candidates**.")

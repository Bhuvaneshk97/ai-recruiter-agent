import streamlit as st
import pandas as pd
import re
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Recruiter Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {background-color:#f8fafc;}

.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
}

.big-title {
    font-size: 34px;
    font-weight: 800;
    color: #4f46e5;
    line-height: 1.4;
    margin-top: 0.5rem;
    margin-bottom: 0.2rem;
}

.sub-title {
    color: #475569;
    font-size: 20px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
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

# ---------------- JD PARSER ----------------
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

# ---------------- SCORING ----------------
def score_candidates(parsed):
    rows = []

    for _, c in df_candidates.iterrows():
        overlap = sum(1 for s in c["skills"] if s in parsed["skills"])
        missing = [s for s in parsed["skills"] if s not in c["skills"]]

        exp = int(c["experience"])
        notice = int(c["notice_days"])

        skill_score = overlap * 12
        exp_score = min(20, exp * 4)

        title_score = 15 if any(
            x in str(c["title"]).lower()
            for x in ["developer", "analyst", "engineer"]
        ) else 8

        location_score = 15 if (
            parsed["location"] == "All" or
            str(c["location"]).lower() == parsed["location"].lower()
        ) else 5

        match_score = min(
            100,
            round(skill_score + exp_score + title_score + location_score, 1)
        )

        availability_score = max(5, 30 - (notice / 2))
        engagement_score = overlap * 5
        exp_bonus = exp * 2

        location_bonus = 10 if (
            parsed["location"] == "All" or
            str(c["location"]).lower() == parsed["location"].lower()
        ) else 3

        interest_score = min(
            100,
            round(
                35 +
                availability_score +
                engagement_score +
                exp_bonus +
                location_bonus,
                1
            )
        )

        final_score = round(
            (match_score * 0.7) + (interest_score * 0.3),
            2
        )

        rows.append({
            "name": c["name"],
            "title": c["title"],
            "experience": exp,
            "location": c["location"],
            "email": c["email"],
            "match_score": match_score,
            "interest_score": interest_score,
            "final_score": final_score,
            "missing_skills": ", ".join(missing) if missing else "None"
        })

    return pd.DataFrame(rows).sort_values("final_score", ascending=False)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🤖 AI Recruiter")
    st.caption("AI-powered candidate discovery & outreach")

    jd = st.text_area(
        "Paste Job Description",
        height=220,
        value="""We are hiring a Power BI Developer with 3+ years experience.
Must have SQL, DAX, Power Query, Power BI Service.
Preferred: Python, Azure.
Location: Chennai / Hybrid."""
    )

    top_n = st.selectbox(
        "Number of Results",
        [20, 50, 100, 250],
        index=2
    )

    run_btn = st.button("🚀 Find Candidates", use_container_width=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="big-title">✨ AI Recruiter Agent</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Find, engage and shortlist top talent instantly.</div>',
    unsafe_allow_html=True
)

# ---------------- MAIN APP ----------------
if run_btn:
    parsed = parse_jd(jd)
    result_df = score_candidates(parsed)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Candidates", len(result_df))
    c2.metric("Top Score", result_df["final_score"].max())
    c3.metric("High Interest", (result_df["interest_score"] >= 85).sum())
    c4.metric("Strong Matches", (result_df["match_score"] >= 80).sum())

    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 JD Parsing",
        "🔍 Candidate Matches",
        "📧 Outreach",
        "🏆 Final Shortlist"
    ])

    with tab1:
        st.subheader("Parsed Job Description")
        st.write(f"**Role:** {parsed['role']}")
        st.write(f"**Experience:** {parsed['experience']}+ years")
        st.write(f"**Location:** {parsed['location']}")
        st.write(f"**Skills:** {', '.join(parsed['skills'])}")

    with tab2:
        st.subheader(f"Top {top_n} Candidate Matches")
        st.dataframe(
            result_df[
                [
                    "name","title","experience","location",
                    "match_score","interest_score",
                    "final_score","missing_skills"
                ]
            ].head(top_n),
            use_container_width=True
        )

    with tab3:
        st.subheader("📧 Candidate Outreach")

        if "open_email" not in st.session_state:
            st.session_state.open_email = None

        if "sent_emails" not in st.session_state:
            st.session_state.sent_emails = {}

        for _, row in result_df.head(10).iterrows():
            candidate_id = row["email"]

            col1, col2, col3, col4 = st.columns([3,2,2,2])

            col1.write(f"**{row['name']}**")
            col1.caption(row["title"])

            col2.write(f"Match: **{row['match_score']}**")
            col3.write(f"Interest: **{row['interest_score']}**")

            if col4.button("📧 Send Email", key=f"open_{candidate_id}", use_container_width=True):
                st.session_state.open_email = candidate_id

            if st.session_state.open_email == candidate_id:
                st.markdown("---")
                st.write(f"### 📩 Compose Email to {row['name']}")
                st.write(f"**To:** {row['email']}")

                st.text_input(
                    "Subject",
                    value=f"{parsed['role']} Opportunity in {parsed['location']}",
                    key=f"subject_{candidate_id}"
                )

                st.text_area(
                    "Message",
                    value=f"""Hi {row['name']},

Your profile looks relevant for a {parsed['role']} opportunity in {parsed['location']}.

Would you be open to discussing this role?

Best regards,
Recruitment Team""",
                    height=220,
                    key=f"body_{candidate_id}"
                )

                send_col, close_col = st.columns(2)

                if send_col.button("🚀 Send Now", key=f"send_{candidate_id}", use_container_width=True):
                    with st.spinner("Sending email..."):
                        time.sleep(1.2)
                    st.session_state.sent_emails[candidate_id] = True
                    st.success("✅ Email sent successfully to candidate!")

                if close_col.button("❌ Close", key=f"close_{candidate_id}", use_container_width=True):
                    st.session_state.open_email = None

                if st.session_state.sent_emails.get(candidate_id, False):
                    if row["interest_score"] >= 85:
                        reply = "Thanks for reaching out. I'm interested. Please share next steps."
                        sentiment = "Highly Interested"
                    elif row["interest_score"] >= 70:
                        reply = "Sounds interesting. Please share compensation and role details."
                        sentiment = "Interested"
                    else:
                        reply = "Thanks. I’m selectively exploring opportunities right now."
                        sentiment = "Neutral"

                    st.info(f"📬 Candidate Reply: {reply}")
                    st.metric("Sentiment", sentiment)

    with tab4:
        st.subheader(f"Top {top_n} Final Ranked Shortlist")

        shortlist = result_df.head(top_n).copy()
        shortlist.insert(0, "rank", range(1, len(shortlist)+1))

        st.dataframe(shortlist, use_container_width=True)

        csv = shortlist.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Shortlist CSV",
            csv,
            "shortlist.csv",
            "text/csv",
            use_container_width=True
        )

else:
    st.info("👉 Paste a Job Description in the sidebar and click Find Candidates.")

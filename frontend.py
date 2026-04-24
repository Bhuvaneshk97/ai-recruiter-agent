import streamlit as st
import pandas as pd
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Recruiter Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #4f46e5;
}
.sub-title {
    color:#475569;
    margin-bottom:18px;
}
.metric-box {
    background:white;
    padding:16px;
    border-radius:14px;
    border:1px solid #eef2f7;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
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

# ---------------- FUNCTIONS ----------------
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
            "email": c["email"],
            "match_score": match_score,
            "interest_score": interest_score,
            "final_score": final_score,
            "missing_skills": ", ".join(missing) if missing else "None"
        })

    return pd.DataFrame(rows).sort_values("final_score", ascending=False)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🤖 AI Recruiter Agent")
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
st.markdown('<div class="big-title">✨ AI Recruiter Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Find, engage and shortlist top talent instantly.</div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
if run_btn:
    parsed = parse_jd(jd)
    result_df = score_candidates(parsed)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Candidates", len(result_df))
    c2.metric("Top Score", result_df["final_score"].max())
    c3.metric("High Interest", (result_df["interest_score"] >= 90).sum())
    c4.metric("Strong Matches", (result_df["match_score"] >= 80).sum())

    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 JD Parsing",
        "🔍 Candidate Matches",
        "📧 Outreach",
        "🏆 Final Shortlist"
    ])

    # ---------------- TAB 1 ----------------
    with tab1:
        st.subheader("Parsed Job Description")
        st.write(f"**Role:** {parsed['role']}")
        st.write(f"**Experience:** {parsed['experience']}+ years")
        st.write(f"**Location:** {parsed['location']}")
        st.write(f"**Skills:** {', '.join(parsed['skills'])}")

    # ---------------- TAB 2 ----------------
    with tab2:
        st.subheader(f"Top {top_n} Candidate Matches")

        st.dataframe(
            result_df[[
                "name","title","experience","location",
                "match_score","interest_score",
                "final_score","missing_skills"
            ]].head(top_n),
            use_container_width=True
        )

    # ---------------- TAB 3 ----------------
    with tab3:
        st.subheader("📧 Candidate Outreach")
        st.caption("Send personalized outreach emails and simulate responses.")

        for idx, row in result_df.head(10).iterrows():

            col1, col2, col3, col4 = st.columns([3,2,2,2])

            with col1:
                st.write(f"**{row['name']}**")
                st.caption(row["title"])

            with col2:
                st.write(f"Match: **{row['match_score']}**")

            with col3:
                st.write(f"Interest: **{row['interest_score']}**")

            with col4:
                open_mail = st.button(
                    "📧 Send Email",
                    key=f"mail_btn_{idx}",
                    use_container_width=True
                )

            if open_mail:
                with st.container(border=True):

                    st.markdown(f"### 📩 Email to {row['name']}")
                    st.write(f"**To:** {row['email']}")

                    subject = st.text_input(
                        "Subject",
                        value=f"{parsed['role']} Opportunity in {parsed['location']}",
                        key=f"sub_{idx}"
                    )

                    default_msg = f"""Hi {row['name']},

Your background in {row['title']} looks relevant for a {parsed['role']} role we are hiring for in {parsed['location']}.

Your experience appears aligned with our requirements, and I’d love to connect to discuss this opportunity.

Would you be open to a quick conversation?

Best regards,
Recruitment Team
"""

                    message = st.text_area(
                        "Message",
                        value=default_msg,
                        height=220,
                        key=f"msg_{idx}"
                    )

                    send_now = st.button(
                        "🚀 Send Now",
                        key=f"send_{idx}",
                        use_container_width=True
                    )

                    if send_now:
                        st.success("✅ Email sent successfully!")

                        if row["interest_score"] >= 90:
                            reply = "Thanks for reaching out. I'm interested and available soon."
                            sentiment = "Highly Interested"
                            updated_score = 95
                        elif row["interest_score"] >= 75:
                            reply = "Thanks for the message. Please share more details about the role."
                            sentiment = "Interested"
                            updated_score = 85
                        else:
                            reply = "Thanks. I’m currently exploring limited opportunities."
                            sentiment = "Neutral"
                            updated_score = 70

                        st.markdown("### 📬 Candidate Response")
                        st.info(reply)

                        cc1, cc2 = st.columns(2)
                        cc1.metric("Sentiment", sentiment)
                        cc2.metric("Updated Interest Score", updated_score)

    # ---------------- TAB 4 ----------------
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
    st.info("👈 Paste a Job Description in the sidebar and click Find Candidates.")

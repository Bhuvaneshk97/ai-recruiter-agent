# 🤖 AI Recruiter Agent

An AI-powered recruiting assistant that takes a Job Description as input, discovers matching candidates, simulates conversational outreach, and returns a ranked shortlist using **Match Score** and **Interest Score**.

---

# 🚀 Live Demo

🔗 Deployed App:  
https://ai-recruiter-agent-chnba8bcpsvy8m8srbjkfh.streamlit.app/

🔗 Source Code:  
https://github.com/Bhuvaneshk97/ai-recruiter-agent

---

# 📌 Problem Statement

Recruiters spend hours reviewing profiles and manually following up with candidates.

This project solves that by automating:

- Job Description parsing
- Candidate discovery
- Candidate matching with explainability
- Simulated outreach to assess interest
- Final recruiter-ready ranked shortlist

---

# ✅ Core Features

## 1. JD Parsing
Extracts structured information from the Job Description:

- Role Title
- Required Skills
- Experience
- Location

## 2. Candidate Discovery
Loads candidate profiles from a **100-candidate CSV dataset**.

## 3. Smart Matching
Each candidate receives a **Match Score** based on:

- Skills overlap
- Experience fit
- Title relevance
- Location fit

## 4. Simulated Conversational Outreach
The system simulates recruiter-candidate conversations and generates an **Interest Score** based on:

- Availability / Notice period
- Positive response intent
- Candidate readiness

## 5. Final Ranked Output
Candidates are ranked using:

Final Score = 0.7 × Match Score + 0.3 × Interest Score

---

# 🏗️ Architecture

```text
Recruiter Inputs JD
        ↓
JD Parser
        ↓
Candidate Dataset (CSV)
        ↓
Scoring Engine
 ├─ Match Score
 ├─ Interest Score
 └─ Explainability
        ↓
Simulated Outreach
        ↓
Ranked Shortlist UI

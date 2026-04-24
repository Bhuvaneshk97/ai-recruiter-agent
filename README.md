# 🤖 AI Recruiter Agent

An AI-powered recruiting assistant that takes a Job Description as input, discovers matching candidates from a large candidate dataset, simulates conversational outreach, and returns a ranked shortlist using **Match Score** and **Interest Score**.

---

# 🚀 Live Demo

### 🔗 Project Site URL
https://ai-recruiter-agent-chnba8bcpsvy8m8srbjkfh.streamlit.app/

### 🔗 GitHub Repository
https://github.com/Bhuvaneshk97/ai-recruiter-agent

---

# 📌 Problem Statement

Recruiters spend hours reviewing profiles, searching for relevant candidates, and manually following up to gauge interest.

This project solves that by automating:

- Job Description parsing
- Candidate discovery from dataset
- Candidate matching with explainability
- Simulated outreach to assess interest
- Final recruiter-ready ranked shortlist

---

# ✅ Core Features

## 1. JD Parsing
Extracts structured requirements from the Job Description:

- Role Title
- Required Skills
- Experience
- Location

---

## 2. Candidate Discovery
Loads and evaluates candidates from a **1000-profile CSV dataset**.

---

## 3. Smart Matching
Each candidate receives a **Match Score** based on:

- Skills overlap
- Experience fit
- Job title relevance
- Location fit

---

## 4. Simulated Conversational Outreach
The system simulates recruiter-candidate conversations and generates an **Interest Score** based on:

- Availability / Notice period
- Positive intent
- Readiness to join

---

## 5. Final Ranked Output
Candidates are ranked using:

```text
Final Score = 0.7 × Match Score + 0.3 × Interest Score

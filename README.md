# AI Recruiter Agent

An AI agent that parses a Job Description, matches candidates, simulates interest scoring, and returns a ranked shortlist.

## Features
- JD parsing
- Candidate matching
- Explainable scores
- Ranked shortlist
- Streamlit UI

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload
streamlit run frontend.py

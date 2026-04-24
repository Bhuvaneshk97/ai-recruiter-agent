# app.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import json
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='AI Recruiter Agent')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class JDRequest(BaseModel):
    jd: str


def extract_skills(text):
    known = ['sql','python','power bi','dax','power query','excel','azure','tableau']
    found = []
    t = text.lower()
    for k in known:
        if k in t:
            found.append(k)
    return found

@app.get('/')
def home():
    return {'message':'AI Recruiter Agent Running'}

@app.post('/shortlist')
def shortlist(req: JDRequest):
    with open('candidates.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)

    skills = extract_skills(req.jd)
    results = []

    for c in candidates:
        overlap = sum(1 for s in c['skills'] if s.lower() in skills)
        skill_score = min(40, overlap * 10)
        exp_score = min(25, c['experience'] * 5)
        title_score = 20 if any(x in c['title'].lower() for x in ['analyst','developer','engineer']) else 10
        location_score = 15 if c['location'].lower() == 'chennai' else 8
        match_score = skill_score + exp_score + title_score + location_score

        interest_score = 90 if c['notice_days'] <= 30 else 65
        final_score = round(match_score * 0.7 + interest_score * 0.3, 2)

        results.append({
            'name': c['name'],
            'title': c['title'],
            'match_score': match_score,
            'interest_score': interest_score,
            'final_score': final_score,
            'why': f"Matched {overlap} skills, {c['experience']} years experience, notice {c['notice_days']} days"
        })

    results.sort(key=lambda x: x['final_score'], reverse=True)
    return results
```

# frontend.py

```python
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='AI Recruiter Agent', layout='wide')
st.title('🤖 AI Recruiter Agent')
st.write('Paste a Job Description and get ranked candidates instantly.')

jd = st.text_area('Job Description', height=220, value='We are hiring a Power BI Developer with 3+ years experience. Must have SQL, DAX, Power Query, Power BI Service. Preferred: Python, Azure. Location: Chennai / Hybrid.')

if st.button('Find Candidates'):
    try:
        res = requests.post('http://localhost:8000/shortlist', json={'jd': jd})
        data = res.json()
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f'Error: {e}')
```

# requirements.txt

```txt
fastapi
uvicorn
pydantic
streamlit
requests
pandas
```

# candidates.json

```json
[
  {
    "name": "Asha Raman",
    "title": "Power BI Developer",
    "experience": 4,
    "skills": ["sql", "power bi", "dax", "python"],
    "location": "Chennai",
    "notice_days": 30
  },
  {
    "name": "Kiran S",
    "title": "Data Analyst",
    "experience": 3,
    "skills": ["sql", "power bi", "power query", "excel"],
    "location": "Bangalore",
    "notice_days": 15
  },
  {
    "name": "Meera V",
    "title": "BI Analyst",
    "experience": 5,
    "skills": ["excel", "tableau", "sql"],
    "location": "Chennai",
    "notice_days": 60
  }
]
```

# README.md

````md
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
````

## API

POST /shortlist

```json
{ "jd": "Power BI Developer with SQL and Python" }
```

## Output

Returns ranked candidates with Match Score, Interest Score, Final Score.

```
```

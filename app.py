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

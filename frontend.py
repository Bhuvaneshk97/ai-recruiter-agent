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

import streamlit as st
import openai
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
import os
import openai

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione dell'autenticazione
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(location='sidebar')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    st.title("Job Ad Generator")

    # Form per l'inserimento dei dati
    with st.form(key='job_ad_form'):
        job_title = st.text_input("Job Title")
        about_company = st.text_area("About the Company")
        #role_overview = st.text_area("Role Overview")
        qualifications = st.text_area("Qualifications")
        years_of_experience = st.text_input("Years of Experience")
        key_responsibilities = st.text_area("Key Responsibilities")
        benefits = st.text_area("Benefits")
        job_type = st.selectbox("Job Type", ["On-site", "Hybrid", "Remote"])
        contract_type = st.selectbox("Contract Type", ["Full-time", "Part-time", "Contract, Internship, Freelance"])
        location = st.text_input("Location")
        
        submit_button = st.form_submit_button(label='Send to AI')

    if submit_button:
        # Generazione del prompt
        prompt = f"""
        I need you to create a job ad based on the following structure:
        Title: {job_title}\n\n
        About the Company: {about_company}\n\n
        Role Overview: Create a brief overview of the role in {job_title} based on the required qualifications {qualifications}\n\n
        Key Responsibilities: Generate a bullet point list of key responsibilities for the role {job_title}\n\n
        Qualifications: Create a bullet list copying the data from {qualifications}\n\n
        Years of experience: {years_of_experience}\n\n
        Create a compelling conclusion to encourage candidates to apply\n\n
        Contract Type: {contract_type}\n\n
        Benefits: list from {benefits}\n\n
        Job Type: {job_type}\n\n
        Location: {location}
        """

        # Configura la chiave API di OpenAI
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Richiesta all'API di OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        # Mostra la risposta sullo schermo
        st.write("### Generated Job Ad")
        st.write(response.choices[0].message.content.strip())

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

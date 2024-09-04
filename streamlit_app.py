import streamlit as st
import openai
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv
import os
import openai
from io import BytesIO
from docx import Document

# Load environment variables from .env
load_dotenv()

# Authentication setup
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Initialize session state variables
if 'job_ad' not in st.session_state:
    st.session_state['job_ad'] = ""

name, authentication_status, username = authenticator.login(location='sidebar')

if authentication_status:
    # Sidebar content
    st.sidebar.image("xantage.jpg", caption="Powered by Xantage", use_column_width=True)
    st.sidebar.write(f'Welcome *{name}*')
    authenticator.logout('Logout', 'sidebar')

    # Main page content
    st.title("Job Ad Generator")

    # Form for job details
    with st.form(key='job_ad_form'):
        job_title = st.text_input("Job Title")
        about_company = st.text_area("About the Company")
        qualifications = st.text_area("Qualifications")
        years_of_experience = st.text_input("Years of Experience")
        benefits = st.text_area("Benefits")
        job_type = st.selectbox("Job Type", ["On-site", "Hybrid", "Remote"])
        contract_type = st.selectbox("Contract Type", ["Full-time", "Part-time", "Contract", "Internship", "Freelance"])
        location = st.text_input("Location")
        
        submit_button = st.form_submit_button(label='Send to AI')

    if submit_button:
        # Prompt generation
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

        # OpenAI API call
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Request to OpenAI's API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        # Store the generated job ad in session state
        st.session_state['job_ad'] = response.choices[0].message.content.strip()
        st.session_state['download_clicked'] = False  # Reset the download state

    # Check if there is a job ad to display
    if st.session_state['job_ad']:
        st.write("### Generated Job Ad")
        st.write(st.session_state['job_ad'])

        # Phase 1: Show "Save ad as .docx" button after displaying the job ad
        save_docx_button = st.button("Save ad as .docx")

        if save_docx_button:
            # Phase 2: Show input for file name
            file_name = st.text_input("Enter the file name (without extension)", "job_ad")

            if file_name:
                # Create a Word document
                doc = Document()
                doc.add_heading('Job Ad', 0)
                doc.add_paragraph(st.session_state['job_ad'])

                # Save the doc to a BytesIO object
                doc_io = BytesIO()
                doc.save(doc_io)
                doc_io.seek(0)  # Move to the beginning of the BytesIO buffer

                # Phase 3: Allow the user to download the .docx file with custom file name
                st.download_button(
                    label="Download",
                    data=doc_io.getvalue(),
                    file_name=f"{file_name}.docx",  # Use the user-specified file name
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    on_click=lambda: st.session_state.update({"download_clicked": True})
                )
    # Show confirmation message after download button is clicked
    if st.session_state['download_clicked']:
        st.success("File downloaded successfully")
        

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


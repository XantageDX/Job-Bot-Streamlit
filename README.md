# Job Ad Generator

**Job Ad Generator** is a web application built with **Streamlit** that leverages **OpenAI's API** to generate professional job ads. Users can securely log in and fill out a form with job details, which are then used by the app to generate a customized job ad.

## Key Features

- **Authentication**: Secure login via username and password, with credentials stored in a YAML file and passwords hashed for security.
- **Job Ad Generation**: Users provide job details such as the title, qualifications, years of experience, contract type, benefits, and more. The app sends these details to OpenAI to generate a professional job ad.
- **OpenAI Integration**: Uses OpenAI's GPT-4 API to automatically generate job ads based on user inputs.
- **Responsive Layout**: A clean, easy-to-use interface that allows users to quickly input information and see the generated job ad instantly.
- **Download Job Ad**: Users can download the generated job ad as a `.docx` file, with the ability to specify a custom file name. After downloading, the user is shown a confirmation message to indicate successful download.

## Project Structure

- `streamlit_app.py`: Main app file containing the logic for authentication and job ad generation.
- `config.yaml`: YAML file used to store user login credentials (username, email, hashed password).
- `.env`: A file that contains the OpenAI API key and other sensitive configurations. **This file is excluded from version control using `.gitignore`.**
- `.gitignore`: Configured to exclude the `.env` file and other sensitive files from version control.

## Requirements

To run this application locally, the following Python libraries are required:

- `streamlit==1.24.0`
- `openai==1.10.0`
- `python-dotenv==1.0.0`
- `streamlit-authenticator==0.2.1`
- `PyYAML==6.0`
- `python-docx==0.8.11`

You can install all dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Setup

**Authentication**

Authentication is managed through a config.yaml file that contains user credentials. Example:
```yaml
credentials:
  usernames:
    user1:
      email: user1@example.com
      name: User One
      password: hashed_password_1
    user2:
      email: user2@example.com
      name: User Two
      password: hashed_password_2

cookie:
  expiry_days: 30
  key: random_generated_key
  name: streamlit_auth_cookie
```

**API Key**

Ensure that you have a ```.env``` file in the root directory with the following configuration:
```bash
OPENAI_API_KEY=your_openai_api_key
````

## Running the Application

To run the application locally, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repository/job-ad-generator.git
    cd job-ad-generator
    ````
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ````
3. Create the ```.env```file with your OpenAI API Key:
    ```bash
    touch .env
    ````
4. Run the application:
    ```bash
    streamlit run streamlit_app.py
    ````

## Features for Saving the Generated Job Ad

After the job ad is generated:
+ A button labeled **"Save ad as .docx"** will appear under the job ad.
+ Upon clicking the button, users can specify a custom file name for the `.docx` file.
+ A download link will be generated, allowing the user to download the job ad in `.docx` format.
+ After the download, a confirmation message **"File downloaded successfully!"** will be displayed to the user.


## Deployment on Streamlit Cloud
To deploy on **Streamlit Cloud**, follow these steps:
1. Push the project to GitHub.
2. Configure environment variables using **Streamlit Secrets** for secure handling of sensitive data.
3. Deploy the repository on **Streamlit Cloud** by following the [Streamlit Cloud Guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started).

## Security
+ User password are hashed before being stored, ensuring secure credential management.
+ API keys and other sensitive information are handled via the `.env` file or **Streamlit Secrets**.
+ The ```.gitignore``` file is configured to ensure sensitive files are not included in the repository.

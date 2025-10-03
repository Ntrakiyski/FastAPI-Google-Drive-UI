This application allows you to connect to your Google Drive account and view your files, neatly organized by format.

CRITICAL NEXT STEP: Before running the app, you MUST create a Google Cloud project, enable the Google Drive API, and create OAuth 2.0 credentials for a "Desktop app". Download the credentials JSON file and save it in the root of your project directory with the filename credentials.json. The application will not work without this file.

Once credentials.json is in place, run the app. You will be prompted to log in with your Google account in the browser to grant access. A token.json file will then be created to keep you logged in for future sessions.


## what is the format of the credentials.json 
The credentials.json file is a Google OAuth 2.0 client configuration file that you download from the Google Cloud Console. Here's the format:

{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}

How to get this file:

Go to Google Cloud Console
Create a new project or select an existing one
Enable the Google Drive API for your project
Go to APIs & Services → Credentials
Click Create Credentials → OAuth client ID
Select Desktop app as the application type
Download the JSON file and rename it to credentials.json
Place it in your project root directory (same level as rxconfig.py)
The file contains your OAuth client ID and secret that allow your app to authenticate users via Google's OAuth flow.


## how to run the app when its on my pc

To run your Reflex app locally on your PC:

Install dependencies (if you haven't already):

pip install -r requirements.txt

Initialize Reflex (first time only):

reflex init

Run the development server:

reflex run

Access the app:

Open your browser and go to: http://localhost:3000
The backend API runs on: http://localhost:8000
Before running, make sure you have:

Your credentials.json file from Google Cloud Console in the project root directory
Python 3.8+ installed
The app will automatically open in your default browser when you run reflex run. Press Ctrl+C in the terminal to stop the server.

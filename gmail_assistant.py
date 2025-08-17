import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Try different possible credential file names
            credential_files = [
                'credentials.json',
                'client_secret_366214454286-sql9rp04t1ig0tsta8ver186sst1h1jt.apps.googleusercontent.com.json'
            ]
            
            creds = None
            for cred_file in credential_files:
                if os.path.exists(cred_file):
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
                        creds = flow.run_local_server(port=0)
                        break
                    except Exception as e:
                        print(f"Error with {cred_file}: {e}")
                        continue
            
            if not creds:
                raise Exception("No valid credentials file found. Please ensure you have a valid Google API credentials file.")
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_emails(service, user_id='me', max_results=200):
    """Fetches the last `max_results` emails from the user's inbox."""
    try:
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        email_data = []
        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            email_data.append(msg)
        return email_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def cluster_emails(emails):
    """Clusters emails based on their subject lines."""
    subjects = []
    for email in emails:
        headers = email['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        if subject:
            subjects.append(subject)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(subjects)

    # You can adjust the number of clusters
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)

    # Create a DataFrame for easier manipulation
    df = pd.DataFrame({'email': emails, 'subject': subjects, 'cluster': kmeans.labels_})
    return df

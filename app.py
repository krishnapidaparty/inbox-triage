from flask import Flask, render_template, redirect, url_for
# Import the functions from your gmail_assistant.py file
from gmail_assistant import get_gmail_service, fetch_emails, cluster_emails

app = Flask(__name__)

@app.route('/')
def index():
    try:
        print("Attempting to get Gmail service...")
        service = get_gmail_service()
        print("Gmail service obtained successfully")
        
        print("Fetching emails...")
        emails = fetch_emails(service)
        if emails:
            print(f"Fetched {len(emails)} emails")
            df = cluster_emails(emails)
            # Convert DataFrame to a list of dictionaries for easy rendering
            clusters = {i: df[df['cluster'] == i].to_dict('records') for i in range(3)}
            return render_template('index.html', clusters=clusters)
        else:
            return "Could not fetch emails."
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"Error: {str(e)}"

@app.route('/archive/<cluster_id>')
def archive_cluster(cluster_id):
    service = get_gmail_service()
    emails = fetch_emails(service)
    if emails:
        df = cluster_emails(emails)
        cluster_emails_df = df[df['cluster'] == int(cluster_id)]
        email_ids = [email['id'] for email in cluster_emails_df['email']]
        
        # The Gmail API uses 'removeLabelIds' with 'INBOX' to archive
        service.users().messages().batchModify(
            userId='me',
            body={'ids': email_ids, 'removeLabelIds': ['INBOX']}
        ).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        print("Starting Flask application...")
        print("Access the application at: http://127.0.0.1:5000")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"Error starting Flask app: {e}")

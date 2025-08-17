from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Replit-specific configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-replit')

@app.route('/')
def index():
    """Main page with demo data for Replit deployment"""
    try:
        # Create demo clusters for Replit deployment
        demo_clusters = {
            0: [
                {
                    'subject': 'Welcome to Inbox Triage Assistant! 📧',
                    'email': {'snippet': 'This is a demo of the email clustering system. In a real deployment, this would show your actual Gmail emails.'}
                },
                {
                    'subject': 'Work Project Updates - Q4 Planning',
                    'email': {'snippet': 'Meeting notes and action items for the upcoming quarter planning session.'}
                },
                {
                    'subject': 'Team Standup - Daily Updates',
                    'email': {'snippet': 'Daily standup meeting agenda and yesterday\'s progress updates.'}
                }
            ],
            1: [
                {
                    'subject': 'Personal: Weekend Plans',
                    'email': {'snippet': 'Planning for the upcoming weekend activities and events.'}
                },
                {
                    'subject': 'Family Dinner Invitation',
                    'email': {'snippet': 'Invitation to family dinner this Sunday at 6 PM.'}
                },
                {
                    'subject': 'Personal Finance Update',
                    'email': {'snippet': 'Monthly budget review and expense tracking summary.'}
                }
            ],
            2: [
                {
                    'subject': 'Special Offer: 50% Off Premium Features',
                    'email': {'snippet': 'Limited time offer on premium subscription features and add-ons.'}
                },
                {
                    'subject': 'Newsletter: Weekly Tech Updates',
                    'email': {'snippet': 'Latest technology news and updates from our weekly newsletter.'}
                },
                {
                    'subject': 'Promotional: New Product Launch',
                    'email': {'snippet': 'Announcing our newest product features and capabilities.'}
                }
            ]
        }
        
        return render_template('index.html', clusters=demo_clusters)
    except Exception as e:
        return f"Error loading demo data: {str(e)}"

@app.route('/archive/<cluster_id>')
def archive_cluster(cluster_id):
    """Demo archive functionality for Replit"""
    try:
        cluster_id = int(cluster_id)
        cluster_names = {
            0: "Work-related emails",
            1: "Personal emails", 
            2: "Promotional emails"
        }
        
        cluster_name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
        
        # In a real deployment, this would archive actual emails
        # For demo purposes, we'll just show a success message
        return f"""
        <html>
        <head><title>Archive Success</title></head>
        <body>
            <h2>✅ Archive Successful!</h2>
            <p>Successfully archived {cluster_name} (Cluster {cluster_id + 1})</p>
            <p><em>Note: This is a demo. In a real deployment with Gmail API credentials, this would actually archive your emails.</em></p>
            <br>
            <a href="/" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">← Back to Inbox</a>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error archiving cluster: {str(e)}"

@app.route('/setup')
def setup_guide():
    """Setup guide for Gmail API integration"""
    return """
    <html>
    <head><title>Gmail API Setup Guide</title></head>
    <body>
        <h1>🔧 Gmail API Setup Guide</h1>
        <p>To use this with your actual Gmail account, follow these steps:</p>
        
        <h2>1. Google Cloud Console Setup</h2>
        <ol>
            <li>Go to <a href="https://console.cloud.google.com/" target="_blank">Google Cloud Console</a></li>
            <li>Create a new project or select existing one</li>
            <li>Enable the Gmail API</li>
            <li>Create OAuth 2.0 credentials</li>
            <li>Download credentials as 'credentials.json'</li>
        </ol>
        
        <h2>2. Local Deployment</h2>
        <ol>
            <li>Clone this repository locally</li>
            <li>Place 'credentials.json' in the project root</li>
            <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
            <li>Run: <code>python app.py</code></li>
        </ol>
        
        <h2>3. Current Demo</h2>
        <p>This Replit deployment shows the interface with demo data. The clustering and archive functionality is fully implemented but uses sample data.</p>
        
        <br>
        <a href="/" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">← Back to Demo</a>
    </body>
    </html>
    """

@app.route('/api/status')
def api_status():
    """API endpoint to check application status"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'environment': 'replit',
        'features': {
            'clustering': 'demo',
            'gmail_integration': 'requires_credentials',
            'archive_functionality': 'demo'
        }
    })

if __name__ == '__main__':
    # Replit-specific configuration
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Inbox Triage Assistant on port {port}")
    print(f"📧 Demo mode: Showing sample email clusters")
    print(f"🌐 Access the app at: https://your-repl-name.your-username.repl.co")
    
    app.run(
        host='0.0.0.0',  # Required for Replit
        port=port,
        debug=debug
    )

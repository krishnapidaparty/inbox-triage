import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import secrets
from datetime import datetime, timedelta
import json

# Import Gmail functions
try:
    from gmail_assistant import get_gmail_service, fetch_emails, cluster_emails
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

app = Flask(__name__)

# Production configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', secrets.token_hex(32)),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
)

# Security headers
Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'font-src': "'self'",
    },
    force_https=True
)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Logging configuration
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/inbox_triage.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Inbox Triage startup')

@app.before_request
def before_request():
    """Log all requests in production"""
    if not app.debug:
        app.logger.info(f'{request.remote_addr} - {request.method} {request.url}')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/')
@limiter.limit("30 per minute")
def index():
    """Main application page with Gmail integration"""
    try:
        if not GMAIL_AVAILABLE:
            return render_template('error.html', 
                error="Gmail integration not available. Please check your credentials.")
        
        # Check if user is authenticated
        if 'gmail_authenticated' not in session:
            return redirect(url_for('auth'))
        
        service = get_gmail_service()
        emails = fetch_emails(service)
        
        if emails:
            df = cluster_emails(emails)
            clusters = {i: df[df['cluster'] == i].to_dict('records') for i in range(3)}
            return render_template('index.html', clusters=clusters)
        else:
            return render_template('error.html', 
                error="No emails found or unable to fetch emails.")
            
    except Exception as e:
        app.logger.error(f'Error in index route: {str(e)}')
        return render_template('error.html', 
            error="An error occurred while processing your emails.")

@app.route('/auth')
@limiter.limit("10 per minute")
def auth():
    """Gmail authentication endpoint"""
    try:
        if GMAIL_AVAILABLE:
            service = get_gmail_service()
            session['gmail_authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('error.html', 
                error="Gmail integration not configured.")
    except Exception as e:
        app.logger.error(f'Authentication error: {str(e)}')
        return render_template('error.html', 
            error="Authentication failed. Please check your credentials.")

@app.route('/archive/<cluster_id>')
@limiter.limit("20 per minute")
def archive_cluster(cluster_id):
    """Archive emails in a specific cluster"""
    try:
        if not GMAIL_AVAILABLE:
            return jsonify({'error': 'Gmail integration not available'}), 400
        
        if 'gmail_authenticated' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        service = get_gmail_service()
        emails = fetch_emails(service)
        
        if emails:
            df = cluster_emails(emails)
            cluster_emails_df = df[df['cluster'] == int(cluster_id)]
            email_ids = [email['id'] for email in cluster_emails_df['email']]
            
            # Archive emails by removing INBOX label
            service.users().messages().batchModify(
                userId='me',
                body={'ids': email_ids, 'removeLabelIds': ['INBOX']}
            ).execute()
            
            app.logger.info(f'Archived {len(email_ids)} emails from cluster {cluster_id}')
            return jsonify({'success': True, 'archived_count': len(email_ids)})
        else:
            return jsonify({'error': 'No emails to archive'}), 400
            
    except Exception as e:
        app.logger.error(f'Archive error: {str(e)}')
        return jsonify({'error': 'Failed to archive emails'}), 500

@app.route('/api/status')
@limiter.limit("60 per minute")
def api_status():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': 'production',
        'gmail_available': GMAIL_AVAILABLE,
        'version': '1.0.0'
    })

@app.route('/api/clusters')
@limiter.limit("30 per minute")
def api_clusters():
    """API endpoint to get email clusters"""
    try:
        if not GMAIL_AVAILABLE:
            return jsonify({'error': 'Gmail integration not available'}), 400
        
        service = get_gmail_service()
        emails = fetch_emails(service)
        
        if emails:
            df = cluster_emails(emails)
            clusters = {}
            for i in range(3):
                cluster_data = df[df['cluster'] == i]
                clusters[i] = {
                    'count': len(cluster_data),
                    'emails': [
                        {
                            'subject': row['subject'],
                            'snippet': row['email'].get('snippet', '')
                        }
                        for _, row in cluster_data.iterrows()
                    ]
                }
            return jsonify(clusters)
        else:
            return jsonify({'error': 'No emails found'}), 404
            
    except Exception as e:
        app.logger.error(f'API clusters error: {str(e)}')
        return jsonify({'error': 'Failed to fetch clusters'}), 500

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.logger.info(f'Starting Inbox Triage Assistant on port {port}')
    app.logger.info(f'Gmail integration available: {GMAIL_AVAILABLE}')
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

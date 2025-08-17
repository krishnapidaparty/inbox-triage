# 📧 Inbox Triage Assistant

An intelligent email management system that uses machine learning to cluster and organize your Gmail inbox, allowing you to archive entire groups of similar emails with one click.

## 🚀 Features

- **Smart Email Clustering**: Uses TF-IDF vectorization and K-Means clustering to group similar emails
- **One-Click Archive**: Archive entire clusters of emails with a single click
- **Gmail API Integration**: Seamlessly connects to your Gmail account
- **Web Interface**: Clean, intuitive web interface built with Flask
- **Real-time Processing**: Fetches and processes your latest 200 emails

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn (TF-IDF, K-Means)
- **Data Processing**: pandas
- **API Integration**: Google Gmail API
- **Frontend**: HTML, CSS, JavaScript

## 📋 Prerequisites

- Python 3.7+
- Gmail account
- Google Cloud Console project with Gmail API enabled

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/krishnapidaparty/inbox-triage.git
   cd inbox-triage
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib scikit-learn pandas Flask
   ```

4. **Set up Google API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials
   - Download the credentials as `credentials.json`
   - Place `credentials.json` in the project root directory

## 🚀 Usage

### Local Deployment

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open your browser to `http://127.0.0.1:5000`
   - First time will trigger Gmail authentication
   - Authorize the application to access your Gmail

3. **Use the interface**
   - View your emails clustered by similarity
   - Click "Archive this cluster" to archive entire groups
   - Refresh to get the latest emails

### Replit Deployment

1. **Fork this repository** to your GitHub account
2. **Import to Replit**:
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl"
   - Choose "Import from GitHub"
   - Select your forked repository
3. **Run the application**:
   - Replit will automatically install dependencies
   - Click "Run" to start the application
   - Access your app at the provided Replit URL

**Note**: The Replit version runs in demo mode with sample data. For full Gmail integration, deploy locally with your Google API credentials.

## 🚀 Production Deployment

### Option 1: Docker Deployment (Recommended)

1. **Prerequisites**:
   - Docker and Docker Compose installed
   - Google API credentials (`credentials.json`)

2. **Quick Deploy**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Manual Docker Deploy**:
   ```bash
   # Build and run with Docker Compose
   docker-compose up -d
   
   # Or build and run manually
   docker build -t inbox-triage .
   docker run -p 8080:8080 -v $(pwd)/credentials.json:/app/credentials.json inbox-triage
   ```

### Option 2: Cloud Platform Deployment

#### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set GOOGLE_CREDENTIALS_FILE=credentials.json
git push heroku main
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/inbox-triage
gcloud run deploy inbox-triage --image gcr.io/PROJECT_ID/inbox-triage --platform managed
```

#### AWS Elastic Beanstalk
```bash
# Create application
eb init inbox-triage --platform python-3.9
eb create inbox-triage-env
eb deploy
```

### Option 3: Traditional Server Deployment

1. **Server Setup**:
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3 python3-pip nginx
   
   # Clone repository
   git clone https://github.com/krishnapidaparty/inbox-triage.git
   cd inbox-triage
   
   # Install Python dependencies
   pip3 install -r requirements_production.txt
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -c gunicorn.conf.py app_production:app
   ```

3. **Configure Nginx**:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/inbox-triage
   sudo ln -s /etc/nginx/sites-available/inbox-triage /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

### Environment Variables

Set these environment variables for production:

```bash
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV="production"
export GOOGLE_CREDENTIALS_FILE="credentials.json"
export DEBUG="False"
```

### Security Considerations

- ✅ **HTTPS**: Always use HTTPS in production
- ✅ **Rate Limiting**: Configured in production app
- ✅ **Security Headers**: Implemented with Flask-Talisman
- ✅ **Input Validation**: All inputs are validated
- ✅ **Logging**: Comprehensive logging for monitoring
- ✅ **Error Handling**: Graceful error handling

## 📁 Project Structure

```
inbox-triage/
├── app.py                 # Main Flask application
├── gmail_assistant.py     # Gmail API integration & ML clustering
├── test_app.py           # Test version without Gmail auth
├── templates/
│   └── index.html        # Web interface template
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## 🔒 Security

- Google API credentials are excluded from version control
- OAuth 2.0 authentication for secure Gmail access
- No email content is stored locally

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gmail API for email access
- scikit-learn for machine learning capabilities
- Flask for the web framework
- Buildathon 2025 for the inspiration

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

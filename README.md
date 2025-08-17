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

#!/bin/bash

echo "🚀 Installing Inbox Triage Assistant dependencies for Replit..."

# Install Python dependencies
pip install Flask==3.1.1
pip install google-api-python-client==2.179.0
pip install google-auth-httplib2==0.2.0
pip install google-auth-oauthlib==1.2.2
pip install scikit-learn==1.7.1
pip install pandas==2.3.1
pip install numpy==2.3.2
pip install scipy==1.16.1

echo "✅ Dependencies installed successfully!"
echo "🎯 Starting the application..."
echo "🌐 Your app will be available at: https://$(echo $REPL_SLUG).$(echo $REPL_OWNER).repl.co"

# Start the application
python app_replit.py

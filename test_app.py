from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Create dummy data for testing
    dummy_clusters = {
        0: [
            {'subject': 'Test Email 1 - Work Related'},
            {'subject': 'Test Email 2 - Work Related'},
            {'subject': 'Test Email 3 - Work Related'}
        ],
        1: [
            {'subject': 'Test Email 4 - Personal'},
            {'subject': 'Test Email 5 - Personal'},
            {'subject': 'Test Email 6 - Personal'}
        ],
        2: [
            {'subject': 'Test Email 7 - Promotional'},
            {'subject': 'Test Email 8 - Promotional'},
            {'subject': 'Test Email 9 - Promotional'}
        ]
    }
    
    return render_template('index.html', clusters=dummy_clusters)

@app.route('/archive/<cluster_id>')
def archive_cluster(cluster_id):
    return f"Archive functionality would archive cluster {cluster_id}"

if __name__ == '__main__':
    try:
        print("Starting Test Flask application...")
        print("Access the application at: http://127.0.0.1:5001")
        app.run(debug=True, host='127.0.0.1', port=5001)
    except Exception as e:
        print(f"Error starting Flask app: {e}")

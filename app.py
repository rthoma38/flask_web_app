import os
import requests
import logging
from flask import Flask, render_template, jsonify
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)

# Secure credentials via environment variables
ZAP_API_KEY = os.getenv("ZAP_API_KEY")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_PASSWORD = os.getenv("JENKINS_PASSWORD")

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_json_data(url, auth=None):
    """Safely fetch JSON data from external APIs."""
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Ensure HTTP success
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return {}
    except ValueError as e:
        logging.error(f"Error decoding JSON from {url}: {e}")
        return {}

@app.route('/api/metrics')
def api_metrics():
    """API endpoint returning security metrics."""
    metrics = {
        'vulnerabilities_detected': 10,
        'ci_cd_status': 'Success',
        'anomalies_flagged': 2
    }
    return jsonify(metrics)

@app.route('/api/anomalies')
def api_anomalies():
    """API endpoint returning anomaly counts."""
    anomalies_data = fetch_json_data('http://127.0.0.1:5001/api/anomalies')
    anomalies = anomalies_data.get('anomalies', 0)
    return jsonify({'anomalies': anomalies})

@app.route('/')
def index():
    """Main dashboard route."""
    # Fetch metrics from Jenkins with authentication
    jenkins_auth = (JENKINS_USER, JENKINS_PASSWORD)
    jenkins_metrics = fetch_json_data('http://localhost:8080/job/midterm/api/json', auth=jenkins_auth)

    last_completed_build = jenkins_metrics.get('lastCompletedBuild', {})
    ci_cd_last_build_url = last_completed_build.get('url', 'N/A')
    ci_cd_last_build_number = last_completed_build.get('number', 'N/A')
    ci_cd_status = 'Unknown'

    # Fetch last build details
    if ci_cd_last_build_url != 'N/A':
        last_build_details = fetch_json_data(f'{ci_cd_last_build_url}/api/json', auth=jenkins_auth)
        ci_cd_status = last_build_details.get('result', 'Unknown')

    # Fetch OWASP ZAP alerts securely
    zap_alerts_url = f'http://localhost:8081/json/core/view/alerts/?baseurl=http://127.0.0.1:5000&apikey={ZAP_API_KEY}'
    zap_alerts = fetch_json_data(zap_alerts_url)

    # Fetch latest anomalies
    anomalies_data = fetch_json_data('http://127.0.0.1:5000/api/anomalies')
    anomalies = anomalies_data.get('anomalies', 0)

    # Process and combine metrics
    vulnerabilities = len(zap_alerts.get('alerts', []))
    
    metrics = {
        'vulnerabilities': vulnerabilities,
        'ci_cd_status': ci_cd_status,
        'ci_cd_last_build_url': ci_cd_last_build_url,
        'ci_cd_last_build_number': ci_cd_last_build_number,
        'anomalies': anomalies
    }

    return render_template('index.html', metrics=metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

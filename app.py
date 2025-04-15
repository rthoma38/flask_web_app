import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def fetch_json_data(url, auth=None):
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return {}
    except ValueError as e:
        print(f"Error decoding JSON from {url}: {e}")
        return {}

@app.route('/api/metrics')
def api_metrics():
    metrics = {
        'vulnerabilities_detected': 10,
        'ci_cd_status': 'Success',
        'anomalies_flagged': 2
    }
    return jsonify(metrics)

@app.route('/api/anomalies')
def api_anomalies():
    anomalies_data = fetch_json_data('http://127.0.0.1:5001/api/anomalies')
    anomalies = anomalies_data.get('anomalies', 0)
    return jsonify({'anomalies': anomalies})

@app.route('/')
def index():
    # Fetch metrics from Jenkins with authentication
    jenkins_auth = ('rthoma38', '112bd83823e0a8eda5316c7ee09109b22e')
    jenkins_metrics = fetch_json_data('http://localhost:8080/job/midterm/api/json', auth=jenkins_auth)

    # Extract additional Jenkins metrics
    last_completed_build = jenkins_metrics.get('lastCompletedBuild', {})
    ci_cd_last_build_url = last_completed_build.get('url', 'N/A')
    ci_cd_last_build_number = last_completed_build.get('number', 'N/A')
    ci_cd_status = 'Unknown'

    # Fetch the details of the last completed build to get its status
    if ci_cd_last_build_url != 'N/A':
        last_build_details = fetch_json_data(f'http://localhost:8080/job/midterm/{ci_cd_last_build_number}/api/json', auth=jenkins_auth)
        ci_cd_status = last_build_details.get('result', 'Unknown')

    # Fetch alerts from OWASP ZAP with API key
    zap_alerts_url = f'http://localhost:8081/json/core/view/alerts/?baseurl=http://127.0.0.1:5000&apikey={zap_api_key}'
    zap_alerts = fetch_json_data(zap_alerts_url)

    # Fetch the latest anomaly count from the new endpoint
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

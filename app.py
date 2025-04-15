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

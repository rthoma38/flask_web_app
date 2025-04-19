import requests
from flask import Flask, render_template, jsonify
from prometheus_client import start_http_server, Summary, Gauge, Counter

app = Flask(__name__)

# Prometheus metrics
REQUEST_TIME = Summary('flask_request_latency_seconds', 'Time spent processing a request')
VULNERABILITY_COUNT = Gauge('flask_vulnerabilities_total', 'Total vulnerabilities detected')
CI_CD_STATUS = Gauge('flask_ci_cd_status', 'CI/CD pipeline status (1=Success, 0=Failed)')
FAILED_AUTH_COUNT = Counter('flask_failed_auth_attempts', 'Number of failed authentication attempts')

@app.route('/metrics')
def prometheus_metrics():
    return jsonify({
        'flask_request_latency_seconds': REQUEST_TIME._value.get(),
        'flask_vulnerabilities_total': VULNERABILITY_COUNT._value.get(),
        'flask_ci_cd_status': CI_CD_STATUS._value.get(),
        'flask_failed_auth_attempts': FAILED_AUTH_COUNT._value.get()
    })

@app.route('/login', methods=['POST'])
def login():
    if request.form.get("password") != "secure123":
        FAILED_AUTH_COUNT.inc()  # Track failed login attempts
        return "Unauthorized", 401
    return "Welcome!", 200

if __name__ == '__main__':
    start_http_server(8000)  # Exposes Prometheus metrics
    app.run(host='0.0.0.0', port=5000, debug=False)

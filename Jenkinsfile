pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-web-app'  // Docker image for your Flask app (already running)
    }

    stages {
        stage('SCM') {
            steps {
                checkout scm  // Checkout your source code from SCM
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Run SonarQube analysis on your source code
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv() {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('OWASP ZAP Dynamic Scan') {
            steps {
                script {
                    echo 'Running OWASP ZAP DAST on Flask Web App...'

                    // Run OWASP ZAP dynamic scan against the already running Flask app container
                    sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock owasp/zap2docker-stable zap-baseline.py -t http://localhost:5000'
                }
            }
        }
    }

    post {
        always {
            // Cleanup resources if necessary (optional)
            echo 'Pipeline finished!'
        }
    }
}

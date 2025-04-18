pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                checkout scm  // Checks out the code from GitHub repository
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv() {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Vulnerability Scan') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image flask_web_app'
            }
        }
    }
}

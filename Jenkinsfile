pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask_web_app'
    }

    stages {
        stage('Install Syft and Grype') {
            steps {
                script {
                    // Install Syft and Grype tools
                    echo 'Installing Syft and Grype...'
                    sh '''
                        curl -sSfL https://github.com/anchore/syft/releases/download/v0.54.0/syft-linux-amd64 -o /usr/local/bin/syft
                        chmod +x /usr/local/bin/syft
                        curl -sSfL https://github.com/anchore/grype/releases/download/v0.40.0/grype-linux-amd64 -o /usr/local/bin/grype
                        chmod +x /usr/local/bin/grype
                    '''
                }
            }
        }

        stage('SCM') {
            steps {
                checkout scm
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

        stage('Generate SBOM with Syft') {
            steps {
                script {
                    echo 'Generating SBOM with Syft for Flask Web App...'
                    sh 'syft flask_web_app:latest -o spdx-json > sbom.json'
                }
            }
        }

        stage('Vulnerability Scan with Grype') {
            steps {
                script {
                    echo 'Running vulnerability scan with Grype on Flask Web App...'
                    sh 'grype flask_web_app:latest --fail-on high'
                }
            }
        }

        stage('Vulnerability Scan with Trivy') {
            steps {
                script {
                    // Run Trivy vulnerability scan on the Docker image built
                    echo 'Running vulnerability scan with Trivy on Flask Web App...'
                    sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:0.61.0 image flask_web_app'
                }
            }
        }
    }
}

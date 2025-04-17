pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                checkout scm  // This checks out the code from GitHub repository
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

        stage('OWASP ZAP Scan') {
            steps {
                script {
                    sh 'python3 zap_scan.py'  // Runs the ZAP scan script
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true  // Archives the ZAP report
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline complete.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}

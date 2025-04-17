node {
    stage('SCM') {
        checkout scm
    }

    stage('SonarQube Analysis') {
        def scannerHome = tool 'SonarQube Scanner'
        withSonarQubeEnv() {
            sh "${scannerHome}/bin/sonar-scanner"
        }
    }

    stage('OWASP ZAP Scan') {
        steps {
            sh '''
                # Assuming you have a Python script (zap_scan.py) to run the ZAP scan
                python3 zap_scan.py
            '''
        }
        post {
            always {
                archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
            }
        }
    }

    stage('Trivy Scan') {
        steps {
            sh '''
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image flask_web_app
            '''
        }
        post {
            always {
                archiveArtifacts artifacts: 'trivy_report.json', allowEmptyArchive: true
            }
        }
    }

    stage('Gitleaks Scan') {
        steps {
            sh 'gitleaks detect --source . --report-path gitleaks_report.json'
        }
        post {
            always {
                archiveArtifacts artifacts: 'gitleaks_report.json', allowEmptyArchive: true
            }
        }
    }

    stage('Archive Reports') {
        steps {
            archiveArtifacts artifacts: '**/zap_report.html, **/trivy_report.json, **/gitleaks_report.json', allowEmptyArchive: true
        }
    }
}

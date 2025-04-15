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

    stage('Vulnerability Scan') {
        echo 'Running vulnerability scan with Trivy on Flask Web App...'
        sh 'trivy image flask_web_app'
    }
}

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

    stage('OWASP ZAP DAST') {
        steps {
            script {
                echo 'Running OWASP ZAP (Iron Bank) DAST against Flask app...'

                // Run ZAP scan using Iron Bank image
                sh '''
                docker run --rm \
                    -v $(pwd):/zap/wrk \
                    ironbank/opensource/owasp-zap/owasp-zap:v2.16.0 \
                    zap-baseline.py -t http://host.docker.internal:5000 \
                    -g gen.conf -r zap_report.html
                '''
            }
        }
    }
}

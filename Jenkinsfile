pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask_web_app:latest'
        SBOM_FILE_TAG = 'syft_sbom.spdx.tag'
        SBOM_FILE_JSON = 'syft_sbom.spdx.json'
        OUTPUT_DIR = 'artifact_reports'  // Directory for storing reports
        NIKTO_REPORT = 'nikto_report.txt'
        ZAP_REPORT = 'zap_report.html'
        GITLEAKS_REPORT = 'gitleaks_report.json'
        NIKTO_TARGET = 'http://localhost:5000'  // Nikto scans localhost
        ZAP_TARGET = 'http://host.docker.internal:5000'  // ZAP scans Docker network
        SONAR_PROJECT_KEY = 'capstone'
        SONARQUBE_URL = 'http://host.docker.internal:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/rthoma38/flask_web_app.git', branch: 'main'
            }
        }

        stage('Prepare Environment') {
            steps {
                sh """
                    mkdir -p ${OUTPUT_DIR}
                    touch ${OUTPUT_DIR}/${ZAP_REPORT}
                    chmod 777 ${OUTPUT_DIR}/${ZAP_REPORT}
                """
            }
        }

        stage('Vulnerability Scan (Trivy)') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image flask_web_app || true'
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    sh """
                        docker run --rm \
                            -v \$(pwd)/${OUTPUT_DIR}:/zap/wrk \
                            registry1.dso.mil/ironbank/opensource/owasp-zap/owasp-zap \
                            zap-baseline.py -t ${ZAP_TARGET} -r /zap/wrk/${ZAP_REPORT} --autooff || true
                    """
                }
            }
        }

        stage('Run Nikto Scan') {
            steps {
                script {
                    sh "nikto -h ${NIKTO_TARGET} -output ${OUTPUT_DIR}/${NIKTO_REPORT} || true"
                }
            }
        }

        stage('Generate SBOM with Syft') {
            steps {
                script {
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            anchore/syft:latest \
                            ${IMAGE_NAME} -o spdx-tag-value > ${OUTPUT_DIR}/${SBOM_FILE_TAG} || true
                    """
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            anchore/syft:latest \
                            ${IMAGE_NAME} -o spdx-json > ${OUTPUT_DIR}/${SBOM_FILE_JSON} || true
                    """
                    echo "Security scan and SBOM generation completed."
                }
            }
        }

        stage('Run Gitleaks Scan') {
            steps {
                script {
                    sh "gitleaks detect --source . --report-path ${GITLEAKS_REPORT} || true"
                }
            }
        }

        stage('Run SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarQube Scanner') {
                    withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            docker run --rm \
                                -v $(pwd):/usr/src \
                                sonarsource/sonar-scanner-cli \
                                -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=$SONARQUBE_URL \
                                -Dsonar.token=$SONAR_TOKEN || true
                        '''
                    }
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${SBOM_FILE_TAG}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${SBOM_FILE_JSON}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${GITLEAKS_REPORT}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${NIKTO_REPORT}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${ZAP_REPORT}", allowEmptyArchive: true
            }
        }
    }
}

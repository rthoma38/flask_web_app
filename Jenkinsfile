pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask_web_app:latest'
        SBOM_FILE_TAG = 'syft_sbom.spdx.tag'
        SBOM_FILE_JSON = 'syft_sbom.spdx.json'
        OUTPUT_DIR = 'artifact_reports'  // Directory for storing reports
        NIKTO_REPORT = 'nikto_report.txt'
        ZAP_REPORT = 'zap_report.html'
        TARGET_URL = 'http://localhost:5000'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/rthoma38/flask_web_app.git', branch: 'main'
            }
        }

        stage('Vulnerability Scan') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image flask_web_app'
            }
        }

        stage('Generate SBOM with Syft') {
            steps {
                script {
                    sh "mkdir -p ${OUTPUT_DIR}"
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            anchore/syft:latest \
                            ${IMAGE_NAME} -o spdx-tag-value > ${OUTPUT_DIR}/${SBOM_FILE_TAG}
                    """
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            anchore/syft:latest \
                            ${IMAGE_NAME} -o spdx-json > ${OUTPUT_DIR}/${SBOM_FILE_JSON}
                    """
                    echo "Security scan and SBOM generation completed."
                }
            }
        }

        stage('Run Gitleaks Scan') {
            steps {
                script {
                    def result = sh(script: 'gitleaks detect --source . --report-path gitleaks_report.json', returnStatus: true)
                    if (result != 0) {
                        echo "Gitleaks found leaks, but continuing the pipeline."
                    } else {
                        echo "Gitleaks scan completed with no leaks."
                    }
                }
            }
        }

        stage('Run Nikto Scan') {
            steps {
                script {
                    sh "nikto -h ${TARGET_URL} -output ${NIKTO_REPORT}"
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    sh """
                        docker run --rm \
                            -v $(pwd):/zap/wrk \
                            registry1.dso.mil/ironbank/opensource/owasp-zap/owasp-zap \
                            zap-baseline.py -t ${TARGET_URL} -r ${ZAP_REPORT}
                    """
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${SBOM_FILE_TAG}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${SBOM_FILE_JSON}", allowEmptyArchive: true
                archiveArtifacts artifacts: 'gitleaks_report.json', allowEmptyArchive: true
                archiveArtifacts artifacts: "${NIKTO_REPORT}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${ZAP_REPORT}", allowEmptyArchive: true
            }
        }
    }
}

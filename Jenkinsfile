pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask_web_app:latest'
        SBOM_FILE_TAG = 'syft_sbom.spdx.tag'
        SBOM_FILE_JSON = 'syft_sbom.spdx.json'
        OUTPUT_DIR = 'artifact_reports'  // Directory for storing reports
        NIKTO_REPORT = 'nikto_report.txt'
        TARGET_URL = 'http://localhost:5000'  // Replace with your actual app URL
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
                    // Create the output directory if it doesn't exist
                    sh "mkdir -p ${OUTPUT_DIR}"

                    // Generate SBOM in SPDX Tag-Value format
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            anchore/syft:latest \
                            ${IMAGE_NAME} -o spdx-tag-value > ${OUTPUT_DIR}/${SBOM_FILE_TAG}
                    """

                    // Generate SBOM in SPDX JSON format
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
                    // Run Gitleaks scan and capture the return code
                    def result = sh(script: 'gitleaks detect --source . --report-path gitleaks_report.json', returnStatus: true)
                    
                    // If there were leaks, log it, but do not fail the pipeline
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
                    // Run Nikto scan and save output to a report
                    sh "nikto -h ${TARGET_URL} -output ${NIKTO_REPORT}"
                }
            }
        }

        stage('Archive Reports') {
            steps {
                // Archive all reports regardless of the outcome
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${SBOM_FILE_TAG}", allowEmptyArchive: true
                archiveArtifacts artifacts: "${OUTPUT_DIR}/${SBOM_FILE_JSON}", allowEmptyArchive: true
                archiveArtifacts artifacts: 'gitleaks_report.json', allowEmptyArchive: true
                archiveArtifacts artifacts: "${NIKTO_REPORT}", allowEmptyArchive: true
            }
        }
    }
}

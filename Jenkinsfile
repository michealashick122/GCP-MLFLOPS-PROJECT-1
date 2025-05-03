pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'vernal-maker-450801-b9'
        GCLOUD_PATH = 'var/jenkins_home/gcloud-cloud-sdk/bin'
    }

    stages {
        stage('Cloning GITHub Reposioory to Jenkins') {
            steps {
                script {
                    echo 'Cloning GITHUB Repository to Jenkins..................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-tocken', url: 'https://github.com/michealashick122/GCP-MLFLOPS-PROJECT-1.git']])
                }
            }
        }

        stage('Setting up Python Virtual Environment and installing dependencies') {
            steps {
                script {
                    echo 'Setting up Python Virtual Environment and installing dependencies.....'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing docker image in GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing docker image in GCR..................'
                        sh '''
                        export PATH=${PATH}:${GCLOUD_PATH}
                        . ${VENV_DIR}/bin/activate
                        export PATH=${PATH}:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/mlops-project-1:latest .
                        docker push gcr.io/${GCP_PROJECT}/mlops-project-1:latest
                        '''
                    }
                }
            }
        }
    }
}
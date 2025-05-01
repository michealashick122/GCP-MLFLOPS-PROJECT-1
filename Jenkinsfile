pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning GITHub Reposioory to Jenkins'){
            steps{
                script{
                    echo 'Cloning GITHUB Repository to Jenkins..................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-tocken', url: 'https://github.com/michealashick122/GCP-MLFLOPS-PROJECT-1.git']])
                }
            }
        }

         stage('Setting up Python Virtual Environment and installing dependencies'){
            steps{
                script{
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
    }
}
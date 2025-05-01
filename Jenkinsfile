pipeline {
    agent any 

    stages {
        stahe('Cloning GITHub Reposioory to Jenkins'){
            steps{
                script{
                    echo 'Cloning GITHUB Repository to Jenkins..................'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-tocken', url: 'https://github.com/michealashick122/GCP-MLFLOPS-PROJECT-1.git']])
                }
            }
        }
    }
}
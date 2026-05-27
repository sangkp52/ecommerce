pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/sangkp52/ecommerce.git'
            }
        }

        stage('Install Backend') {
            steps {
                sh 'cd backend && pip install -r requirements.txt'
            }
        }

        stage('Install Frontend') {
            steps {
                sh 'cd frontend && npm install'
            }
        }

        stage('Unit Test') {
            steps {
                sh 'cd backend && pytest'
            }
        }

        stage('Frontend Test') {
            steps {
                sh 'cd frontend && npm test -- --watchAll=false'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy Staging') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }
}
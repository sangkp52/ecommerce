pipeline {
    agent any

    stages {
        stage('Install Backend') {
            steps {
                sh 'cd backend && pip install -r requirements.txt'
            }
        }

        stage('Install Python') {
            agent {
            docker {
                image 'python:3.11'
            }
        }
            steps {
                sh '''
                cd backend
                pip install -r requirements.txt
                '''
            }
        }

        stage('Install Frontend') {
             steps {
                sh '''
                apt-get update
                apt-get install -y python3 python3-pip
                pip3 install -r backend/requirements.txt
                '''
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
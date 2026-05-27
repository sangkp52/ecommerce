pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend - Install & Test') {
            agent {
                docker {
                    image 'python:3.11'
                }
            }
            steps {
                sh '''
                    cd backend
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }

        stage('Frontend - Install & Test') {
            agent {
                docker {
                    image 'node:18'
                }
            }
            steps {
                sh '''
                    cd frontend
                    npm install
                    npm test -- --watchAll=false
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }
}
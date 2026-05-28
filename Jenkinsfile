pipeline {
    agent any

    tools {
        dockerTool 'docker' 
    }

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
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
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
                    npm test -- --watchAll=false || true
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
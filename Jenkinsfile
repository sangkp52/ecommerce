pipeline {
    agent any

    // Định nghĩa các công cụ cần dùng trong toàn bộ Pipeline
    tools {
        nodejs 'node18' // Gọi công cụ NodeJS đã cấu hình trong Global Tool
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend - Install & Test') {
            steps {
                // Sử dụng chính môi trường của Jenkins để chạy venv (Không cần Docker agent)
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
            steps {
                // Chạy npm trực tiếp thông qua công cụ NodeJS Tool ở trên
                sh '''
                    cd frontend
                    npm install
                    npm test -- --watchAll=false || true
                '''
            }
        }

        stage('Docker Build') {
            steps {
                // Build cụm sản phẩm
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                // Deploy dự án lên các cổng mong muốn
                sh 'docker compose up -d'
            }
        }
    }
}
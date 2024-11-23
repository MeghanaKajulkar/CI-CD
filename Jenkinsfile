pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = "yourdockerhubusername/myapp"  // Replace with your Docker Hub username/repository
        DOCKER_CREDENTIALS = 'dockerhub-credentials'  // Jenkins credentials ID for Docker Hub (set up in Jenkins)
    }
    stages {
        // Checkout code from SCM
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        // Install Python dependencies
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip uninstall werkzeug -y'  // Uninstall werkzeug if it's problematic
                bat 'pip install werkzeug==2.3.3'  // Install specific version of werkzeug
                bat 'pip install -r requirements.txt'  // Install other dependencies listed in requirements.txt
            }
        }

        // Run tests (unit tests or any other type)
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'python -m unittest discover -s tests'  // Adjust if you use pytest or other testing framework
            }
        }

        // Build Docker image
        stage('Build Docker Image') {
            when {
                expression { return currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t ${DOCKER_REGISTRY}:latest .'  // Build Docker image with the tag
            }
        }

        // Push Docker image to Docker registry
        stage('Push Docker Image') {
            when {
                expression { return currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Pushing Docker image to Docker registry...'
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    bat "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"  // Login to Docker registry using Jenkins credentials
                    bat 'docker push ${DOCKER_REGISTRY}:latest'  // Push the Docker image to the registry
                }
            }
        }
    }
}

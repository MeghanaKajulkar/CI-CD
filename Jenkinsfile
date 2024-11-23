pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'meghanamk24/feedbackapp'  // Replace with your Docker Hub username/repository
        DOCKER_CREDENTIALS = 'docker-hub-credentials'  // The Jenkins credential ID you created for Docker Hub
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

        // Login to Docker Hub
        stage('Login to Docker Hub') {
            steps {
                script {
                    // Securely login to Docker Hub using Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", 
                                                        usernameVariable: 'DOCKER_USER', 
                                                        passwordVariable: 'DOCKER_PASS')]) {
                        bat "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                    }
                }
            }
        }

        // Build Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    bat "docker build -t ${DOCKER_REGISTRY}:latest ."
                }
            }
        }

        // Run Docker Container
        stage('Run Docker Container') {
            steps {
                script {
                    // Run the container (e.g., map ports if necessary or run in detached mode)
                    bat "docker run -d -p 8000:8000 ${DOCKER_REGISTRY}:latest"
                }
            }
        }

        // Push Docker Image
        stage('Push Docker Image') {
            steps {
                script {
                    // Tag and push the image to Docker Hub
                    bat "docker tag ${DOCKER_REGISTRY}:latest ${DOCKER_REGISTRY}:latest"
                    bat "docker push ${DOCKER_REGISTRY}:latest"
                }
            }
        }
    }
}

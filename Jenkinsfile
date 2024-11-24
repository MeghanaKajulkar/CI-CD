pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'meghanamk24/feedbackapp'  // Replace with your Docker Hub username/repository
        DOCKER_CREDENTIALS = 'docker-hub-credentials'  // Jenkins credential ID for Docker Hub
        DEPLOYMENT_FILE = 'deployment.yaml'  // Path to your Kubernetes deployment file
    }

    stages {
        // Checkout code from SCM
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        // Install Python Dependencies
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat '''
                    pip uninstall werkzeug -y
                    pip install werkzeug==2.3.3
                    pip install -r requirements.txt
                '''
            }
        }

        // Run Tests
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat 'python -m unittest discover -s tests'  // Update this command for pytest if necessary
            }
        }

        // Login to Docker Hub
        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        bat "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                    }
                }
            }
        }

        // Build Docker Image
        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKER_REGISTRY}:latest ."
            }
        }

        // Push Docker Image to Docker Hub
        stage('Push Docker Image') {
            steps {
                echo "Pushing Docker image to registry..."
                bat "docker push ${DOCKER_REGISTRY}:latest"
            }
        }

        // Deploy to Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying to Kubernetes...'
                    
                    // Apply the Kubernetes deployment file
                    bat "kubectl apply -f ${DEPLOYMENT_FILE}"

                    // Verify the deployment
                    bat "kubectl get pods"
                }
            }
        }

        // Cleanup Old Docker Containers
        stage('Cleanup Old Containers') {
            steps {
                script {
                    echo 'Cleaning up old Docker containers...'
                    bat """
                        docker ps -a -q --filter "name=feedbackapp" | ForEach-Object { docker stop $_; docker rm $_ }
                    """
                }
            }
        }
    }
}

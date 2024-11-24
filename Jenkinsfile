pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'meghanamk24/feedbackapp'  // Replace with your Docker Hub username/repository
        DOCKER_CREDENTIALS = 'docker-hub-credentials'  // Jenkins credential ID for Docker Hub
        DEPLOYMENT_FILE = 'deployment.yaml'
        APP_PORT = ''  // Dynamically allocated port placeholder
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

        // Find an Available Port
        stage('Find Available Port') {
            steps {
                script {
                    def randomPort = 8000 + (Math.random() * 1000).toInteger()  // Generate random port between 8000 and 9000
                    def isPortAvailable = false

                    // Check if port is available using a simple shell script
                    while (!isPortAvailable) {
                        def result = bat(script: "netstat -an | findstr ':${randomPort}'", returnStatus: true)
                        echo "Checking port: ${randomPort} (result: ${result})"
                        if (result != 0) {
                            isPortAvailable = true
                        } else {
                            randomPort = 8000 + (Math.random() * 1000).toInteger()  // Regenerate if port is already in use
                            echo "Port ${randomPort} is in use, trying again..."
                        }
                    }

                    // Ensure the port is assigned to APP_PORT
                    env.APP_PORT = randomPort
                    echo "Found available port: ${env.APP_PORT}"
                }
            }
        }

        // Run Docker Container with Dynamic Port
        stage('Run Docker Container') {
            steps {
                echo "Running Docker container on port ${env.APP_PORT}..."
                bat "docker run -d -p ${env.APP_PORT}:8000 ${DOCKER_REGISTRY}:latest"
            }
        }

        // Push Docker Image to Registry
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

                    // Extract namespace from the deployment file
                    def namespace = powershell(returnStdout: true, script: """
                        (Get-Content ${DEPLOYMENT_FILE} | Select-String -Pattern 'namespace:').Line.Split(':')[1].Trim()
                    """).trim()

                    // Apply the deployment file and verify deployment
                    bat "kubectl apply -f ${DEPLOYMENT_FILE}"
                    bat "kubectl get pods --namespace=${namespace}"
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

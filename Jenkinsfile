pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'meghanamk24/feedbackapp' // Replace with your Docker Hub username/repository
        DOCKER_CREDENTIALS = 'docker-hub-credentials' // Jenkins credential ID for Docker Hub
        DEPLOYMENT_FILE = 'deployment.yaml'
        APP_PORT = '' // Dynamically allocated port placeholder
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
                bat 'python -m unittest discover -s tests' // Update this command for pytest if necessary
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
                    def port = powershell(returnStdout: true, script: """
                        $usedPorts = Get-NetTCPConnection -State Listen | Select-Object -ExpandProperty LocalPort
                        $availablePorts = (8000..9000) | Where-Object { \$usedPorts -notcontains \$_ }
                        if (\$availablePorts.Count -gt 0) {
                            return \$availablePorts[0]
                        } else {
                            return 'No available ports'
                        }
                    """).trim()

                    if (port == 'No available ports') {
                        error 'No available port found in the range 8000-9000'
                    }
                    env.APP_PORT = port
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
                bat """
                    docker tag ${DOCKER_REGISTRY}:latest ${DOCKER_REGISTRY}:latest
                    docker push ${DOCKER_REGISTRY}:latest
                """
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
                    bat """
                        docker ps -a -q --filter "name=feedbackapp" | ForEach-Object { docker stop $_; docker rm $_ }
                    """
                }
            }
        }
    }
}

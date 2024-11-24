pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'meghanamk24/feedbackapp'  // Replace with your Docker Hub username/repository
        DOCKER_CREDENTIALS = 'docker-hub-credentials'  // The Jenkins credential ID you created for Docker Hub
        DEPLOYMENT_FILE = 'deployment.yaml'
        APP_PORT = ''  // Placeholder for dynamically allocated port
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
                    bat "docker build -t ${DOCKER_REGISTRY}:latest ."
                }
            }
        }

        // Find an Available Port
        stage('Find Available Port') {
            steps {
                script {
                    // Use PowerShell to find an available port (adjust port range as needed)
                    def port = powershell(returnStdout: true, script: """
                        $usedPorts = Get-NetTCPConnection -State Listen | Select-Object -ExpandProperty LocalPort
                        $availablePorts = (8000..9000) | Where-Object { $_ -notin $usedPorts }
                        $availablePorts[0]
                    """).trim()
                    APP_PORT = port
                    echo "Found available port: ${APP_PORT}"
                }
            }
        }

        // Run Docker Container with Dynamic Port
        stage('Run Docker Container') {
            steps {
                script {
                    bat "docker run -d -p ${APP_PORT}:8000 ${DOCKER_REGISTRY}:latest"
                }
            }
        }

        // Push Docker Image
        stage('Push Docker Image') {
            steps {
                script {
                    bat "docker tag ${DOCKER_REGISTRY}:latest ${DOCKER_REGISTRY}:latest"
                    bat "docker push ${DOCKER_REGISTRY}:latest"
                }
            }
        }

        // Deploy to Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying to Kubernetes...'

                    // Extract namespace using PowerShell
                    def namespace = powershell(returnStdout: true, script: """
                        (Get-Content ${DEPLOYMENT_FILE} | Select-String -Pattern 'namespace:').Line.Split(':')[1].Trim()
                    """).trim()

                    // Apply the deployment file
                    bat "kubectl apply -f ${DEPLOYMENT_FILE}"

                    // Verify the deployment in the extracted namespace
                    bat "kubectl get pods --namespace=${namespace}"
                }
            }
        }

        // Cleanup Old Containers (Optional)
        stage('Cleanup Old Containers') {
            steps {
                script {
                    bat "docker ps -a -q --filter 'name=feedbackapp' | xargs -r docker stop"
                    bat "docker ps -a -q --filter 'name=feedbackapp' | xargs -r docker rm"
                }
            }
        }
    }
}

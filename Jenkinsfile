pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                echo "Cloning the repository..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                bat 'python -m unittest discover -s tests'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building the Docker image..."
                bat 'docker build -t feedback-app:latest .'
            }
        }

        stage('Deploy Application') {
            steps {
                echo "Deploying the application..."
                script {
                    bat """
                    docker ps -q -f name=feedback-app-container | for /f "tokens=*" %i in ('more') do docker stop %i && docker rm %i
                    docker run -d -p 5000:5000 --name feedback-app-container feedback-app:latest
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                echo "Performing health check..."
                script {
                    def response = bat(
                        script: "curl --silent --fail http://localhost:5000 || echo 'DOWN'",
                        returnStdout: true
                    ).trim()
                    if (response.contains('DOWN')) {
                        error "Application health check failed!"
                    } else {
                        echo "Application is running successfully!"
                    }
                }
            }
        }
    }
}


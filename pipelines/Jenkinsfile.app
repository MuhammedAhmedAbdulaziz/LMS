// ----------------------------------------
// Jenkinsfile for Application (Monorepo)
// ----------------------------------------
pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        // --- DOCKER CONFIG ---
        DOCKER_HUB_USER = 'azoooz'
        APP_NAME        = 'library-app'
        IMAGE_TAG       = 'latest' 
        
        // --- AWS CONFIG ---
        CLUSTER_NAME    = 'azoz-eks'
        AWS_REGION      = 'eu-west-1'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // We check out the 'main' branch where all folders exist
                git branch: 'main', url: 'https://github.com/MuhammedAhmedAbdulaziz/LMS.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // CRITICAL: Switch to 'app' directory to find Dockerfile
                    dir('app') {
                        echo "Building Docker Image inside app/ folder..."
                        sh "docker build -t ${DOCKER_HUB_USER}/${APP_NAME}:${IMAGE_TAG} ."
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-credi', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_HUB_USER}/${APP_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withAWS(credentials: 'aws-credi', region: "${AWS_REGION}") {
                    script {
                        // CRITICAL: Switch to 'k8s' directory to find YAMLs
                        dir('k8s') {
                            echo "Deploying Kubernetes manifests from k8s/ folder..."
                            
                            // 1. Connect to Cluster
                            sh "aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}"
                            
                            // 2. Apply all YAMLs in this folder
                            sh "kubectl apply -f ."

                            // 3. Force Restart to pull new image
                            sh "kubectl rollout restart deployment/flask-app-deployment -n library-app"
                            sh "kubectl rollout status deployment/flask-app-deployment -n library-app"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi ${DOCKER_HUB_USER}/${APP_NAME}:${IMAGE_TAG} || true"
        }
    }
}
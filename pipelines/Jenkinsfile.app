//----------------------------------------
// Jenkins Pipeline for CI/CD of Library App
//----------------------------------------   
pipeline {
    agent any

    // This ensures the job listens to the Webhook you created
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
        
        // --- GIT CONFIG ---
        REPO_URL        = 'https://github.com/MuhammedAhmedAbdulaziz/LMS.git'
        CODE_BRANCH     = 'migrate-to-postgres' // The code to build
        CONFIG_BRANCH   = 'eks-migration'       // The K8s YAML files
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout the application code
                git branch: "${CODE_BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image..."
                    sh "docker build -t ${DOCKER_HUB_USER}/${APP_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    echo "Pushing to DockerHub..."
                    // Login using the 'docker-credi' credentials from Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker-credi', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_HUB_USER}/${APP_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                // Using the 'Pipeline: AWS Steps' plugin (your preferred method)
                withAWS(credentials: 'aws-credi', region: "${AWS_REGION}") {
                    script {
                        // Create a separate directory for K8s manifests
                        dir('k8s_deploy') {
                            // 1. Fetch the YAML files from the config branch
                            git branch: "${CONFIG_BRANCH}", url: "${REPO_URL}"
                            
                            // 2. Connect to the EKS Cluster
                            sh "aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}"
                            
                            // 3. Apply the YAML configuration
                            // (Note: Since the tag is always 'latest', this alone might not trigger an update)
                            sh "kubectl apply -f k8s/"

                            // 4. FORCE UPDATE (Crucial for 'latest' tag)
                            // This kills the old pods so they pull the new image
                            sh "kubectl rollout restart deployment/flask-app-deployment -n library-app"
                            
                            // 5. Wait for the rollout to complete to ensure success
                            sh "kubectl rollout status deployment/flask-app-deployment -n library-app"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up: Remove the image from the Jenkins server to save disk space
            sh "docker rmi ${DOCKER_HUB_USER}/${APP_NAME}:${IMAGE_TAG} || true"
        }
    }
}

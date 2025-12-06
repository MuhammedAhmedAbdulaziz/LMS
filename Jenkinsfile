pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "eu-west-1"        
        CLUSTER_NAME = 'azoz-eks'

    }

    stages {

        stage('Terraform Init') {
            steps {
                echo "Running terraform init..."
                withAWS(credentials: 'aws-credi', region: 'eu-west-1') {
                    sh "terraform init"
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                echo "Validating terraform files..."
                sh "terraform validate"
            }
        }

        stage('Terraform Plan') {
            steps {
                echo "Running terraform plan..."
                withAWS(credentials: 'aws-credi', region: 'eu-west-1') {
                    sh "terraform plan -out=tfplan"
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                echo "Applying terraform changes..."
                withAWS(credentials: 'aws-credi', region: 'eu-west-1') {
                    sh "terraform apply -auto-approve tfplan"
                }
            }
        }

       
    }

    post {
        success {
            echo "Terraform deployment successful!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}

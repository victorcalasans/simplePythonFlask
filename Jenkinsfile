pipeline {
    agent any

    environment {
        IMAGE_TAG = "0.${env.BUILD_ID}"
    }

    stages {

        stage('Build') {
            steps {
                sh "docker build -t simple-python-flask:${IMAGE_TAG} ."
            }
        }

        stage('Test') {
            steps {
                sh """
                docker run --rm simple-python-flask:${IMAGE_TAG} \
                nosetests --with-xunit --with-coverage \
                --cover-package=project test_users.py
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline executada com sucesso!"
        }
        failure {
            echo "Pipeline falhou!"
        }
    }
}
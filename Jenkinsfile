podTemplate(
    containers: [
        containerTemplate(
            name: 'docker',
            image: 'docker:24.0',
            command: 'sleep',
            args: '99d',
            privileged: true
        ),
        containerTemplate(
            name: 'openjdk',
            image: 'openjdk:11',
            command: 'sleep',
            args: '99d',
            privileged: true
        )
    ],
    volumes: [
        hostPathVolume(
            hostPath: '/var/run/docker.sock',
            mountPath: '/var/run/docker.sock'
        )
    ]
) {
    node(POD_LABEL) {

        env.IMAGE_TAG = "0.${env.BUILD_ID}"

        try {

            container('docker') {

                stage('Checkout') {
                    git 'http://192.168.88.20:3000/victor/simplePythonFlask.git'
                }

                stage('Build') {
                    sh "docker build -t simple-python-flask:${env.IMAGE_TAG} ."
                }

                stage('Test') {
                    sh """
                    docker run --rm simple-python-flask:${env.IMAGE_TAG} \
                    nosetests --with-xunit --with-coverage \
                    --cover-package=project test_users.py
                    """

                    sh """
                    docker tag simple-python-flask:${env.IMAGE_TAG} \
                    192.168.88.20:8082/simple-python-flask:${env.IMAGE_TAG}
                    """
                }
            }

            container('openjdk') {

                stage('SonarQube Analysis') {
                    script {
                        def sonarScannerPath = tool 'SonarScanner'

                        withSonarQubeEnv('SonarQube') {
                            sh """
                            ${sonarScannerPath}/bin/sonar-scanner \
                            -Dsonar.projectKey=courseCatalog \
                            -Dsonar.sources=.
                            """
                        }
                    }
                }
            }

            container('docker') {

                stage('Push Image') {
                    withCredentials([usernamePassword(
                        credentialsId: 'jenkins_docker',
                        usernameVariable: 'REG_USER',
                        passwordVariable: 'REG_PASS'
                    )]) {
                        sh """
                        docker login 192.168.88.20:8082 -u $REG_USER -p $REG_PASS
                        docker push 192.168.88.20:8082/simple-python-flask:${env.IMAGE_TAG}
                        """
                    }
                }
            }

            echo "Pipeline executada com sucesso!"

        } catch (err) {
            echo "Pipeline falhou!"
            throw err
        }
    }
}
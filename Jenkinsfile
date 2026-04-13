podTemplate(
    containers: [
        containerTemplate(
            name: 'docker',
            image: 'docker:24.0',
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

        container('docker') {

            try {

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

                    sh "docker tag simple-python-flask:${env.IMAGE_TAG} 192.168.88.20:8082/simple-python-flask:${env.IMAGE_TAG}"
                }

                stage('Push Image') {
                    withCredentials([usernamePassword(
                        credentialsId: 'b9149541-0be1-4e1d-8ae5-a11bb56ea106',
                        usernameVariable: 'REG_USER',
                        passwordVariable: 'REG_PASS'
                    )]) {
                        sh """
                        docker login 192.168.88.20:8082 -u $REG_USER -p $REG_PASS
                        docker push 192.168.88.20:8082/simple-python-flask:${env.IMAGE_TAG}
                        """
                    }
                }

                echo "Pipeline executada com sucesso!"

            } catch (err) {
                echo "Pipeline falhou!"
                throw err
            }
        }
    }
}
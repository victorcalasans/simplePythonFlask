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

        try {

            env.IMAGE_TAG = "0.${env.BUILD_ID}"

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
                }
            }

            echo "Pipeline executada com sucesso!"

        } catch (err) {
            echo "Pipeline falhou!"
            throw err
        }
    }
}
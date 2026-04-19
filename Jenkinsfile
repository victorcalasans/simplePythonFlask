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
      image: 'eclipse-temurin:11',
      command: 'sleep',
      args: '99d',
      privileged: true
    ),
    containerTemplate(
      name: 'kubectl',
      image: 'alpine',
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

      // ✅ AGORA CORRETO: usando container kubectl
      container('kubectl') {

        stage('Deploy Image'){
          withKubeConfig([
            credentialsId: 'k3s-serviceaccount',
            serverUrl: 'https://192.168.88.30:6443',
          ]){

            sh 'apk update && apk add --no-cache curl'

            sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'

            sh 'chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl'

            sh 'sleep 5'

            sh """
            kubectl set image deployment/web \
            simplepythonflask=192.168.88.20:8082/simple-python-flask:${IMAGE_TAG} \
            -n homolog
            """

            sh 'sleep 5'
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
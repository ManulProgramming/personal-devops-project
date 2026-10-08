pipeline {
    agent any

    environment {
        STUDENT_NAME    = 'Dmitriy'
        STUDENT_SURNAME = 'Boyarkin'
        STUDENT_GROUP   = 'IT2-2312'
        STUDENT_ID      = '37752'
        IMAGE_NAME      = 'boyarkin-dmitriy-devops'
        CONTAINER_NAME  = 'boyarkin-dmitriy-container'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
                echo "Student: ${STUDENT_NAME} ${STUDENT_SURNAME}"
                echo "Group: ${STUDENT_GROUP}"
                echo "Student ID: ${STUDENT_ID}"
            }
        }

        stage('Build') {
            steps {
                sh 'bash -n scripts/Boyarkin_Dmitriy_system.sh'
                sh 'python3 -m py_compile app/main.py'
                sh 'chmod +x scripts/Boyarkin_Dmitriy_system.sh'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m unittest discover -s tests -v'
                sh './scripts/Boyarkin_Dmitriy_system.sh'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME} .'
                sh 'docker images ${IMAGE_NAME}'
            }
        }

        stage('Docker Run') {
            steps {
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh '''
                    docker run -d --name ${CONTAINER_NAME} \
                      -e STUDENT_NAME=${STUDENT_NAME} \
                      -e STUDENT_SURNAME=${STUDENT_SURNAME} \
                      -e STUDENT_GROUP=${STUDENT_GROUP} \
                      -e STUDENT_ID=${STUDENT_ID} \
                      ${IMAGE_NAME}
                '''
                sh 'sleep 3'
                sh 'docker ps --filter name=${CONTAINER_NAME}'
                sh 'docker logs ${CONTAINER_NAME}'
            }
        }
    }

    post {
        success { echo 'Pipeline finished successfully' }
        failure { echo 'Pipeline FAILED - check the stage that turned red' }
    }
}

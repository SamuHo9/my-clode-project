pipeline {
    agent any 

    environment {
        // ดึง username/password จาก Credentials ID: docker-hub-creds ที่เราสร้างใน Jenkins
        DOCKER_HUB = credentials('docker-hub-creds')
        IMAGE_NAME = "my-cloud-project" // ชื่อเดียวกับที่ Build ในเครื่อง
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm // ดึงโค้ดจาก GitHub ที่เราเชื่อมไว้ [cite: 1149]
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    // ใช้ตัวแปร $DOCKER_HUB_USR เพื่อระบุชื่อเจ้าของ Image
                    sh "docker build -t ${DOCKER_HUB_USR}/${IMAGE_NAME}:${BUILD_NUMBER} ./app"
                    sh "docker build -t ${DOCKER_HUB_USR}/${IMAGE_NAME}:latest ./app"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // ล็อกอินและผลัก Image ขึ้นไปบน Docker Hub ออนไลน์ [cite: 1155, 1161]
                    sh "echo $DOCKER_HUB_PSW | docker login -u $DOCKER_HUB_USR --password-stdin"
                    sh "docker push ${DOCKER_HUB_USR}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_HUB_USR}/${IMAGE_NAME}:latest"
                }
            }
        }
    }
}
// phase 3
pipeline {
    agent any 

    environment {
        DOCKER_HUB = credentials('docker-hub-creds')
        IMAGE_NAME = "my-cloud-project"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_HUB_USR}/${IMAGE_NAME}:${BUILD_NUMBER} ./app"
                    sh "docker build -t ${DOCKER_HUB_USR}/${IMAGE_NAME}:latest ./app"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    sh 'echo "$DOCKER_HUB_PSW" | docker login -u "$DOCKER_HUB_USR" --password-stdin'
                    sh "docker push ${DOCKER_HUB_USR}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_HUB_USR}/${IMAGE_NAME}:latest"
                }
            }
        }

        // เพิ่ม Stage ใหม่สำหรับ Phase 3 ตรงนี้ครับ
        stage('Deploy (IaC)') {
            steps {
                script {
                    echo "==============================================="
                    echo "Phase 3: Provisioning Infrastructure (Terraform)"
                    echo "==============================================="
                    dir('terraform') {
                        sh 'terraform init'
                        sh 'terraform apply -auto-approve'
                    }

                    echo "==============================================="
                    echo "Phase 3: Configuring Environment (Ansible)"
                    echo "==============================================="
                    dir('ansible') {
                        sh 'ansible-playbook -i inventory playbook.yml'
                    }
                }
            }
        }
    }
}
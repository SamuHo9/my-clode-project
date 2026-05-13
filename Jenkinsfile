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

        stage('K8s Deployment') {
            steps {
                script {
                    echo "==============================================="
                    echo "Phase 4: Deploying Application to Kubernetes"
                    echo "==============================================="

                    // คัดลอก kubeconfig จาก Jenkins home มาที่ workspace
                    sh 'mkdir -p .kube'
                    sh 'cp /root/.kube/config .kube/config'

                    // แก้ server URL ให้ชี้ไป host.docker.internal:6443 (Docker Desktop K8s)
                    sh "sed -i 's|server: https://127.0.0.1:[0-9]*|server: https://host.docker.internal:6443|g' .kube/config"

                    // Deploy ผ่าน bitnami/kubectl container (--network host ไม่ได้ผลบน Windows)
                    sh "docker run --rm -v ${WORKSPACE}/.kube/config:/root/.kube/config -v ${WORKSPACE}:/work -w /work bitnami/kubectl:latest apply -f k8s/deployment.yaml --validate=false --insecure-skip-tls-verify=true"

                    sh "docker run --rm -v ${WORKSPACE}/.kube/config:/root/.kube/config -v ${WORKSPACE}:/work -w /work bitnami/kubectl:latest apply -f k8s/service.yaml --validate=false --insecure-skip-tls-verify=true"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs above."
        }
    }
}
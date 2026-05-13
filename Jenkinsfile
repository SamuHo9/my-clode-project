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
                    // สั่งนำ Manifest ไฟล์ไปรันบน Cluster
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/service.yaml'
                }
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
                    
                    // 1. เตรียมไฟล์ Kubeconfig ภายใน workspace เพื่อให้คอนเทนเนอร์ kubectl มองเห็น
                    sh 'mkdir -p .kube'
                    sh 'cp /root/.kube/config .kube/config'
                    
                    // 2. ใช้ Docker สั่งรัน kubectl บนชั้นเน็ตเวิร์กของโฮสต์โดยตรง ทะลวงผ่านทุก Firewall
                    sh 'docker run --rm --network host -v ${WORKSPACE}/.kube/config://.kube/config -v ${WORKSPACE}:/work -w /work --env KUBECONFIG=//.kube/config bitnami/kubectl:latest apply -f k8s/deployment.yaml --validate=false --insecure-skip-tls-verify=true'
                    sh 'docker run --rm --network host -v ${WORKSPACE}/.kube/config://.kube/config -v ${WORKSPACE}:/work -w /work --env KUBECONFIG=//.kube/config bitnami/kubectl:latest apply -f k8s/service.yaml --validate=false --insecure-skip-tls-verify=true'
                }
            }
        }
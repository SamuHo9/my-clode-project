# Note API - Cloud & Serverless Project

โปรเจกต์นี้พัฒนาระบบ RESTful API สำหรับจัดการบันทึกข้อความ (Notes) ด้วย Python/Flask และเตรียมระบบ CI/CD Pipeline แบบครบวงจร (Jenkins, Docker, Terraform, Ansible, Kubernetes, Prometheus, Grafana)

## โครงสร้างโปรเจกต์ (Repository Structure)
- `app/` : ซอร์สโค้ดของ API, ไฟล์ `requirements.txt` และ `Dockerfile`
- `terraform/` : สคริปต์สำหรับเตรียมโครงสร้างพื้นฐาน (IaC)
- `ansible/` : Playbook สำหรับตั้งค่าระบบและสภาพแวดล้อม
- `k8s/` : Manifest ไฟล์สำหรับ Deploy ลง Kubernetes (Deployment, Service)
- `monitoring/` : ไฟล์การตั้งค่า Prometheus และ Grafana Dashboard

## กลยุทธ์การจัดการกิ่ง (Git Branching Strategy)
โปรเจกต์นี้ใช้กลยุทธ์การแตกกิ่งดังนี้:
- **`main`** : กิ่งหลักสำหรับโค้ดที่พร้อมใช้งานจริงบน Production (Stable)
- **`dev`** : กิ่งสำหรับการพัฒนาและรวบรวมฟีเจอร์ใหม่
- **`feature/*`** : กิ่งย่อยสำหรับพัฒนาแต่ละฟีเจอร์ (เช่น `feature/add-auth`)

## วิธีการติดตั้งและทดสอบบนเครื่อง (Local Setup Instructions)

### 1. การรันด้วย Python โดยตรง
```bash
cd app
pip install -r requirements.txt
python app.py
```

เข้าถึงได้ที่: http://localhost:5000

### 2. การรันด้วย Docker (แนะนำ)
สร้างและรัน Container:
```bash
docker build -t my-clode-project .
docker run -d -p 5000:5000 --name note-container my-clode-project
```

เข้าถึงได้ที่: http://localhost:5000

## การใช้งาน API
- **GET /notes** - ดูรายการโน้ตทั้งหมด
- **POST /notes** - สร้างโน้ตใหม่ (ส่ง JSON: `{"title": "...", "content": "..."}`)
- **GET /metrics** - ดูสถิติการทำงาน (สำหรับ Prometheus)

## โครงสร้าง Pipeline (CI/CD Pipeline Flow)
1. **Checkout** - ดึงโค้ดจาก Git Repository
2. **Build** - สร้าง Docker Image
3. **Push** - อัปโหลด Image ขึ้น Docker Hub
4. **Provision** - สร้าง/อัปเดต Infrastructure ด้วย Terraform
5. **Deploy** - Deploy Application ลง Kubernetes Cluster ด้วย Ansible

### 3. การรัน Jenkins

รหัส Jenkins initialAdminPassword
72e9154504f34794b39a42a2f649da96

รัน docker jenkins อันนี้ไฟล์ yml
docker-compose up -d 



# 1. ใช้ Base Image เป็น Python เวอร์ชันเล็ก (slim) เพื่อให้ Image มีขนาดเล็กและโหลดเร็ว
FROM python:3.10-slim

# 2. กำหนดโฟลเดอร์ทำงานภายใน Container
WORKDIR /app

# 3. ก๊อปปี้ไฟล์ requirements.txt เข้าไปก่อน เพื่อติดตั้ง Library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. ก๊อปปี้โค้ดทั้งหมด (app.py) เข้าไปใน Container
COPY . .

# 5. เปิดพอร์ต 5000 ให้ภายนอกสามารถเชื่อมต่อเข้ามาได้
EXPOSE 5000

# 6. คำสั่งรันแอปพลิเคชันเมื่อ Container สตาร์ท
CMD ["python", "app.py"]
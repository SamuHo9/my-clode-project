from flask import Flask, jsonify, request
from prometheus_client import generate_latest, Counter

app = Flask(__name__)

# สร้างตัวเก็บสถิติว่ามีคนยิง Request เข้ามากี่ครั้ง (สำหรับ Grafana ในอนาคต)
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

# ข้อมูลจำลองในหน่วยความจำ (In-memory Data)
notes = [
    {"id": 1, "title": "First Note", "content": "Hello Cloud and Serverless!"}
]

# Endpoint 1: ดึงข้อมูลโน้ตทั้งหมด (GET) และสร้างโน้ตใหม่ (POST)
@app.route('/notes', methods=['GET', 'POST'])
def manage_notes():
    if request.method == 'GET':
        REQUEST_COUNTER.labels(method='GET', endpoint='/notes').inc()
        return jsonify(notes)
    
    elif request.method == 'POST':
        REQUEST_COUNTER.labels(method='POST', endpoint='/notes').inc()
        new_note = request.get_json()
        new_note['id'] = len(notes) + 1
        notes.append(new_note)
        return jsonify({"message": "Note created successfully!", "note": new_note}), 201

# Endpoint 2: สำหรับให้ Prometheus เข้ามาดูดข้อมูลสถิติ (Metrics)
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์ที่พอร์ต 5000 และเปิดให้ทุกหมายเลข IP เข้าถึงได้ (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)
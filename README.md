# DL-05-RAG System Development II

สถานการณ์จำลองปัญหา RAG 1–9 พร้อมวิเคราะห์สาเหตุและแนวทางแก้ ใช้ Python standard library โดยไม่เรียก LLM API

## ติดตั้งและรันบน Windows

1. ติดตั้ง Python 3.12 แล้วเปิด `SETUP.cmd`
2. เปิด `RUN.cmd` เพื่อรันแล็ปและสร้างไฟล์ที่จำเป็น

เปิด `RUN.cmd -Chat` เพื่อเลือกสถานการณ์ผ่านเมนู หรือรัน `python main.py`
รายละเอียดโจทย์ต้นฉบับอยู่ใน [README-UPSTREAM.md](README-UPSTREAM.md) ชุดโค้ดนี้มีสถานการณ์ 1–9

แต่ละ repository ทำงานแยกกัน ใช้ `.venv` และ `.cache` ภายในโฟลเดอร์ตัวเอง
การดาวน์โหลดโมเดลครั้งแรกต้องใช้อินเทอร์เน็ต ผู้ที่มี dependencies อยู่แล้วรัน `python run_assignment.py` ได้โดยตรง
ผลลัพธ์ index และ log จะสร้างในเครื่องเมื่อรัน และถูกกันออกจาก Git ด้วย `.gitignore`

## แหล่งที่มา

โค้ดและข้อมูลตั้งต้นจาก [repository รายวิชา](https://github.com/aproot-en/Advanced-Topic-in-Computer-Software-Course), commit `c0db2ac52be9646e68b25d90ce87ac2526dc9a3d`
มีการปรับให้รันบน Windows และเพิ่มตัวเปิดงาน รายละเอียด pipeline อยู่ใน source code และ labs ของแต่ละงาน

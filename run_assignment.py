"""Run the nine supplied problem simulations and save each transcript."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DISCUSSION = [
    ("Hallucination", "ไม่มี context แต่ยังสร้างคำตอบ", "ตรวจว่ามีหลักฐานก่อนตอบ และปฏิเสธเมื่อไม่มีข้อมูล"),
    ("Vocabulary / Position", "คำต่างรูปและลำดับคำทำให้ BoW ไม่สะท้อนความหมาย", "ใช้ semantic embeddings และพิจารณาลำดับคำ; ตัวอย่างนี้เพียงสาธิตข้อจำกัดของ BoW"),
    ("Data Quality", "ข้อมูลซ้ำ ช่องว่าง และสัญลักษณ์รบกวน", "normalize แล้ว deduplicate พร้อมตรวจข้อความที่เสียหาย"),
    ("Chunking", "chunk ใหญ่ปะปนหลายเรื่อง ส่วน chunk เล็กตัดบริบท", "เปรียบเทียบขนาดและ overlap; วิธี split ตามช่องว่างในตัวอย่างมีข้อจำกัดกับภาษาไทย"),
    ("Metadata", "ข้อความคล้ายกันแต่ระดับภาษาไม่ตรงงาน", "filter lang หรือหมวดก่อนจัดอันดับตาม similarity"),
    ("Re-ranking", "ผลที่ตรงรายละเอียดอาจอยู่ต่ำในการค้นรอบแรก", "ดึง candidates มาก่อนแล้วจัดอันดับละเอียด; ตัวอย่างใช้คะแนนคำที่กำหนด ไม่ใช่ cross-encoder"),
    ("Faithfulness", "ค้น context ถูก แต่ตัวสร้างคำตอบเปลี่ยนตัวเลขหรือเงื่อนไข", "เทียบคำตอบกับ context และตรวจรายละเอียดสำคัญก่อนใช้"),
    ("Configuration", "เปิดปิด component แล้วเส้นทางประมวลผลเปลี่ยน", "บันทึก configuration ทุกครั้งและเปรียบเทียบโดยเปลี่ยนทีละตัว"),
    ("Evaluation", "ค่า k ที่ต่างกันทำให้ตัดสินผลค้นหาต่างกัน", "ใช้ชุดเฉลยและ Hit@k, MRR, nDCG; ตัวอย่างนี้แสดงหลักการ ยังไม่คำนวณ metrics ทั้งชุด"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat", action="store_true", help="Open the interactive problem menu")
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.chat:
        subprocess.run([sys.executable, "main.py"], check=True)
        return
    from data_loader import load_qa, categories
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    outcomes = []
    for number in range(1, 10):
        run = subprocess.run([sys.executable, "main.py", str(number)], capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
        transcript = run.stdout + "\n" + run.stderr
        (evidence / f"problem{number:02d}.txt").write_text(transcript, encoding="utf-8")
        outcomes.append({"problem": number, "exit_code": run.returncode})
        print(f"Problem {number}:", "PASS" if run.returncode == 0 else "FAIL", flush=True)
        if run.returncode:
            raise RuntimeError(f"See evidence/problem{number:02d}.txt")
    data = load_qa()
    stamp = datetime.now(timezone.utc).isoformat()
    summary = {"executed_at_utc": stamp, "records": len(data),
               "categories": categories(data), "languages": sorted({d['lang'] for d in data}),
               "problems": outcomes, "simulation_only": True}
    (evidence / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    table = ["| ข้อ | ปัญหา | สาเหตุ/สิ่งที่สังเกต | แนวทางแก้ |", "|---:|---|---|---|"]
    for i, (name, cause, solution) in enumerate(DISCUSSION, 1):
        table.append(f"| {i} | {name} | {cause} | {solution} |")
    report = f"""# ใบงาน 5: Prob-RAG — บันทึกผลการทดลองจริง

แหล่งโค้ด: aproot-en/Advanced-Topic-in-Computer-Software-Course, commit c0db2ac
รันเมื่อ (UTC): {stamp}

## วัตถุประสงค์และวิธีทำ

ทดลองสคริปต์ปัญหา RAG ข้อ 1–9 จาก repository โดยใช้ sex_q_a.txt ชุดเดียวกัน
อ่านได้จริง {len(data)} Q&A ใน {len(categories(data))} หมวด
รัน `python main.py 1` ถึง `python main.py 9` และบันทึก stdout/stderr แยกข้อ
ทั้ง 9 สคริปต์จบด้วย exit code 0

## การวิเคราะห์แต่ละปัญหา

{chr(10).join(table)}

## การตีความผล

สคริปต์เป็นสถานการณ์จำลองเพื่ออธิบายแนวคิด ไม่ได้ฝึก Transformer หรือเรียก LLM จริง
ตัวอย่าง hallucination และ generation ที่ผิดถูกเขียนให้ผิดโดยตั้งใจ
ส่วน reranking ใช้กฎให้น้ำหนักคำ จึงไม่ใช่หลักฐานว่าโมเดล cross-encoder แม่นขึ้น
Problem 09 แสดงช่วง chunk และหลัก Top-k; ไม่ได้วัด accuracy หรือ metrics จริงบนทุกคำถาม
ผลเปรียบเทียบ retrieval เชิงตัวเลขจริงอยู่ในงาน DL-04-RAG System Development I

## การแก้ไขโค้ดต้นฉบับ

ต้นฉบับ main.py import problem10_debug_scripts แต่ไม่มีไฟล์นั้นอยู่ใน repository
สำเนานี้ตัด import และเมนู Problem 10 แล้วปรับช่วงตัวเลือกเป็น 0–9
คงสคริปต์ปัญหา 1–9 ไว้ตามต้นฉบับ โดยไม่สร้างผลของปัญหาที่ไม่มีไฟล์

## หลักฐานและการรันซ้ำ

- `evidence/problem01.txt` ถึง `problem09.txt`: ผลจริงแยกข้อ
- `evidence/summary.json`: จำนวนข้อมูล รายการหมวด ภาษา และ exit code
- `python run_assignment.py`: รันครบและสร้างรายงานนี้ใหม่
- `python main.py`: เปิดเมนูให้เลือกข้อ; 0 คือรันครบทุกข้อ

เอกสารนี้จัดเตรียมด้วยความช่วยเหลือของ AI ผู้เรียนควรอ่าน transcript และอธิบายตัวอย่างแต่ละข้อได้ก่อนส่ง
"""
    (ROOT / "REPORT.md").write_text(report, encoding="utf-8")
    print("Saved REPORT.md and evidence/summary.json", flush=True)


if __name__ == "__main__":
    main()

# ใบงาน 5: Prob-RAG

อ่าน REPORT.md เพื่อดูผลจริงและการวิเคราะห์ปัญหา 1–9
หลักฐานแยกข้ออยู่ใน evidence/problem01.txt ถึง problem09.txt

ดับเบิลคลิก RUN.cmd เพื่อทดลองครบและสร้างรายงานใหม่
ใช้ `RUN.cmd -Chat` เพื่อเลือกเมนูด้วยตนเอง
งานนี้ใช้ Python standard library จึงรันโดยตรงได้ด้วย `python run_assignment.py`
หรือ `python main.py` เพื่อเปิดเมนู และ `python main.py 4` เพื่อทดลองเฉพาะข้อ 4

สำเนานี้แก้ main.py ที่ import ไฟล์ Problem 10 ซึ่งไม่มีอยู่ แล้วเพิ่มเครื่องมือเก็บ log และสร้างรายงาน
README-UPSTREAM.md เก็บคำอธิบายต้นฉบับ; ข้อความด้านล่างเป็นคำอธิบายเดิมซึ่งมีบางจุดกล่าวถึง 10 simulations
แต่ไฟล์ที่มีจริงคือข้อ 1–9

source และ dataset มาจาก aproot-en/Advanced-Topic-in-Computer-Software-Course ที่ commit c0db2ac
ตัวอย่างเป็น simulation ที่เขียนพฤติกรรมผิดไว้เพื่อการเรียนรู้ ไม่ได้เรียก LLM จริง

---

# DL-05-RAG System Development II

This project demonstrates 9 common problems in LLM and RAG (Retrieval-Augmented Generation) systems. All simulations use the same real dataset, sex_q_a.txt, which is a Thai sexual health question-answer knowledge base. This allows each problem to be tested with real data instead of isolated sample data.

# Structure:

```text
RAG-Project/
├── sex_q_a.txt                    # Raw data / RAG Knowledge Base
├── data_loader.py                 # Shared parser: sex_q_a.txt -> list of dict
├── main.py                        # Main menu for running each problem
├── problem01_hallucination.py     # Hallucination / answer without supporting context
├── problem02_transformer.py       # Vocabulary Mismatch + Token Position
├── problem03_data_quality.py      # Duplicate / Noise / Normalization
├── problem04_chunking.py          # Chunk Size / Overlap
├── problem05_metadata.py          # Metadata Filtering
├── problem06_reranking.py         # Top-k / Re-ranking
├── problem07_generation.py        # Correct Retrieval but incorrect Generation
├── problem08_config.py            # RAG Configuration
└── problem09_evaluation.py        # Chunk & Retrieval Evaluation
```

# Dataset:
The project uses one shared Knowledge Base containing Thai questions and answers about sexual health, consent, anatomy, and related laws.

The dataset contains 391 entries, covering 6 main categories and 3 language styles: formal, casual, and slang.

Each entry has three lines:
```text

[หมวด: <category>]
or
[หมวด: <category> | ภาษา: <variant>]

Q: <question>
A: <answer>

```
# Summary:

| # | Problem | Main Idea |
|---|---------|-----------|
| 1 | Hallucination | The LLM answers without supporting context. |
| 2 | Vocabulary Mismatch / Position | BoW cannot handle different wording or word order well. |
| 3 | Data Quality | Duplicate and noisy data reduce data quality. |
| 4 | Chunking | Poor chunk size or overlap can lose context. |
| 5 | Metadata Filtering | Similar content may have the wrong metadata. |
| 6 | Re-ranking | First-stage retrieval may rank the best document too low. |
| 7 | Faithfulness | Retrieval is correct, but generation changes important information. |
| 8 | RAG Configuration | Configuration controls which RAG components are active. |
| 9 | Evaluation | Measure chunking and retrieval with numerical metrics. |

All ten simulations use the same real Knowledge Base through `data_loader.py`. 
This allows different LLM and RAG problems to be tested using the same dataset and pipeline.






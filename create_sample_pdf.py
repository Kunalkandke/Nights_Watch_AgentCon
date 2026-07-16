"""
Creates sample_case_dummy.pdf — a realistic hospital discharge summary
for testing the MedComply AI 4-agent workflow.
"""
import fitz  # PyMuPDF
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_case_dummy.pdf")

# ── Page setup ────────────────────────────────────────────────────────────────
doc = fitz.open()
page = doc.new_page(width=595, height=842)  # A4

# ── Helpers ───────────────────────────────────────────────────────────────────
def text(page, x, y, s, size=10, bold=False, color=(0,0,0)):
    fontname = "helv" if not bold else "hebo"
    page.insert_text((x, y), s, fontsize=size, fontname=fontname, color=color)

def hline(page, y, x0=40, x1=555, width=0.5, color=(0.7,0.7,0.7)):
    page.draw_line((x0, y), (x1, y), color=color, width=width)

def rect_fill(page, x0, y0, x1, y1, color):
    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=color, fill=color)

# ── Header banner ─────────────────────────────────────────────────────────────
rect_fill(page, 0, 0, 595, 70, (0.48, 0.17, 0.17))   # dark red
text(page, 40, 25, "CITY GENERAL HOSPITAL & RESEARCH CENTRE", size=14, bold=True, color=(1,1,1))
text(page, 40, 43, "12, Medical Campus Road, Pune - 411001  |  Tel: 020-2456-7890", size=8, color=(0.9,0.8,0.8))
text(page, 40, 57, "NABH Accredited  |  ISO 9001:2015 Certified", size=8, color=(0.9,0.8,0.8))

# Document title bar
rect_fill(page, 0, 70, 595, 92, (0.95, 0.93, 0.91))
text(page, 40, 85, "DISCHARGE SUMMARY", size=13, bold=True, color=(0.48,0.17,0.17))
text(page, 420, 85, "Doc No: CGH/DS/2024/03847", size=8, color=(0.5,0.5,0.5))

y = 105

# ── Patient details box ───────────────────────────────────────────────────────
text(page, 40, y, "PATIENT INFORMATION", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

fields_left = [
    ("Patient Name",    "Mr. Rajesh Kumar Sharma"),
    ("Age / Gender",    "42 Years / Male"),
    ("Date of Birth",   "15-June-1982"),
    ("Blood Group",     "B+ve"),
    ("Aadhaar No.",     "XXXX-XXXX-3847  (masked)"),
]
fields_right = [
    ("UHID",            "CGH-2024-08347"),
    ("Ward / Bed",      "Orthopaedic Ward — Bed 14B"),
    ("Admission Date",  "12-March-2024"),
    ("Discharge Date",  "20-March-2024"),
    ("Total Stay",      "8 Days"),
]
for i, ((lk, lv), (rk, rv)) in enumerate(zip(fields_left, fields_right)):
    text(page, 40,  y, lk + ":", size=8, bold=True)
    text(page, 145, y, lv, size=8)
    text(page, 310, y, rk + ":", size=8, bold=True)
    text(page, 415, y, rv, size=8)
    y += 14

hline(page, y)
y += 12

# ── Treating team ─────────────────────────────────────────────────────────────
text(page, 40, y, "TREATING TEAM", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

team = [
    ("Consultant Surgeon",       "Dr. Anjali Mehta (MS Ortho, DNB)",   "Reg. No. MCI-42891"),
    ("Anaesthesiologist",        "Dr. Vikram Nair (MD Anaesthesia)",    "Reg. No. MCI-38712"),
    ("Resident Physician",       "Dr. Priya Desai (MBBS, Intern)",     "Reg. No. MCI-56023"),
]
for role, name, reg in team:
    text(page, 40,  y, role + ":", size=8, bold=True)
    text(page, 175, y, name, size=8)
    text(page, 390, y, reg, size=8, color=(0.5,0.5,0.5))
    y += 13
hline(page, y)
y += 12

# ── Diagnosis ────────────────────────────────────────────────────────────────
text(page, 40, y, "DIAGNOSIS", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

diagnoses = [
    ("Primary",   "Fracture of Right Femur Shaft (AO Type 32-B2)"),
    ("Secondary", "Mild Traumatic Brain Injury (GCS 14/15 on admission)"),
    ("Comorbid",  "Type 2 Diabetes Mellitus (HbA1c: 7.8%)"),
    ("Comorbid",  "Hypertension — Grade 1 (BP 148/92 mmHg on admission)"),
]
for dtype, ddesc in diagnoses:
    text(page, 40,  y, dtype + ":", size=8, bold=True)
    text(page, 115, y, ddesc, size=8)
    y += 13
hline(page, y)
y += 12

# ── History ──────────────────────────────────────────────────────────────────
text(page, 40, y, "PRESENTING HISTORY", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

history = (
    "Patient Mr. Rajesh Kumar Sharma, a 42-year-old male, presented to the Emergency Department on "
    "12-March-2024 following a road traffic accident (RTA). Patient was a pillion rider on a two-wheeler "
    "that collided with a truck at approximately 60 km/h. Patient was brought by ambulance with complaints "
    "of severe pain in the right thigh, inability to bear weight, and brief loss of consciousness (~2 min). "
    "On arrival: GCS 14/15, BP 148/92 mmHg, Pulse 102/min, SpO2 98% on room air. X-Ray right femur "
    "confirmed displaced mid-shaft fracture. CT Head showed no intracranial haemorrhage. Referred to "
    "Orthopaedic Surgery for definitive management. MLC (Medico-Legal Case) registered: MLC/2024/0843."
)
# Word-wrap manually (PyMuPDF textbox)
r = fitz.Rect(40, y, 555, y + 80)
page.insert_textbox(r, history, fontsize=8, fontname="helv", color=(0,0,0))
y += 82
hline(page, y)
y += 12

# ── Surgical procedure ───────────────────────────────────────────────────────
text(page, 40, y, "SURGICAL PROCEDURE", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

surg_rows = [
    ("Procedure",        "Open Reduction and Internal Fixation (ORIF) — Right Femur"),
    ("Date & Time",      "14-March-2024 | 09:30 AM"),
    ("Duration",         "2 hours 45 minutes"),
    ("Anaesthesia",      "Spinal + IV sedation"),
    ("Implant Used",     "Titanium Intramedullary Nail — 11mm x 380mm (Synthes, Lot #TN-2847)"),
    ("Blood Loss",       "Approx. 350 mL  |  Transfusion: 1 unit PRBC"),
    ("Complications",    "Nil intraoperative"),
    ("Post-op X-Ray",    "Satisfactory reduction and alignment confirmed"),
]
for k, v in surg_rows:
    text(page, 40,  y, k + ":", size=8, bold=True)
    text(page, 145, y, v, size=8)
    y += 13
hline(page, y)
y += 12

# ── Medications ──────────────────────────────────────────────────────────────
text(page, 40, y, "MEDICATIONS AT DISCHARGE", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

# Table header
rect_fill(page, 40, y-2, 555, y+12, (0.96, 0.93, 0.91))
text(page, 42,  y+8, "Medicine", size=8, bold=True)
text(page, 200, y+8, "Dose", size=8, bold=True)
text(page, 290, y+8, "Frequency", size=8, bold=True)
text(page, 390, y+8, "Duration", size=8, bold=True)
text(page, 470, y+8, "Route", size=8, bold=True)
y += 18

meds = [
    ("Tab. Diclofenac Sodium 50mg",   "50 mg",   "Twice daily (after food)",  "5 days",   "Oral"),
    ("Tab. Gabapentin 300mg",          "300 mg",  "Three times daily",          "10 days",  "Oral"),
    ("Tab. Metformin 500mg",           "500 mg",  "Twice daily (with meals)",   "Ongoing",  "Oral"),
    ("Tab. Amlodipine 5mg",            "5 mg",    "Once daily",                 "Ongoing",  "Oral"),
    ("Tab. Pantoprazole 40mg",         "40 mg",   "Once daily (empty stomach)", "14 days",  "Oral"),
    ("Tab. Aspirin 75mg",              "75 mg",   "Once daily",                 "30 days",  "Oral"),
    ("Inj. Enoxaparin 40mg",          "40 mg",   "Once daily (subcutaneous)",  "7 days",   "SC"),
    ("Cal + D3 Tablet (Shelcal)",      "1 tab",   "Once daily",                 "3 months", "Oral"),
]
for i, (med, dose, freq, dur, route) in enumerate(meds):
    if i % 2 == 0:
        rect_fill(page, 40, y-2, 555, y+11, (0.99, 0.98, 0.97))
    text(page, 42,  y+8, med,   size=7.5)
    text(page, 200, y+8, dose,  size=7.5)
    text(page, 290, y+8, freq,  size=7.5)
    text(page, 390, y+8, dur,   size=7.5)
    text(page, 470, y+8, route, size=7.5)
    y += 13
hline(page, y)
y += 12

# ── Investigations ───────────────────────────────────────────────────────────
text(page, 40, y, "KEY INVESTIGATIONS", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

investigations = [
    ("Haemoglobin",     "9.8 g/dL (Low)",       "CBC — 12-Mar"),
    ("WBC Count",       "11,200 /μL (High)",     "CBC — 12-Mar"),
    ("Platelet Count",  "2.1 Lac /μL (Normal)",  "CBC — 12-Mar"),
    ("HbA1c",           "7.8% (Elevated)",       "Biochemistry"),
    ("Serum Creatinine","1.1 mg/dL (Normal)",    "Biochemistry"),
    ("PT / INR",        "13.2 sec / 1.1 (Normal)","Coagulation"),
    ("CT Head",         "No intracranial bleed",  "Radiology — 12-Mar"),
    ("X-Ray Femur",     "Displaced mid-shaft #",  "Radiology — 12-Mar"),
    ("Post-op X-Ray",   "Nail in situ, aligned",  "Radiology — 15-Mar"),
]
for i in range(0, len(investigations), 3):
    row = investigations[i:i+3]
    for j, (test, val, date) in enumerate(row):
        xoff = 40 + j * 172
        text(page, xoff,      y, test + ":", size=7.5, bold=True)
        text(page, xoff,      y+10, val, size=7.5)
        text(page, xoff,      y+20, date, size=7, color=(0.5,0.5,0.5))
    y += 33
hline(page, y)
y += 12

# ── Condition at discharge ───────────────────────────────────────────────────
text(page, 40, y, "CONDITION AT DISCHARGE", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

cond = [
    ("General Condition",  "Stable, ambulatory with crutches"),
    ("Wound Status",       "Clean, dry, sutures intact — to be removed on Day 14"),
    ("Pain Score (VAS)",   "3/10 at rest, 5/10 on movement"),
    ("Neurological",       "GCS 15/15, no focal deficits"),
    ("Diabetes",           "Blood glucose controlled — FBS 118 mg/dL on discharge"),
    ("Hypertension",       "BP 132/82 mmHg — controlled on Amlodipine"),
]
for k, v in cond:
    text(page, 40,  y, k + ":", size=8, bold=True)
    text(page, 175, y, v, size=8)
    y += 13
hline(page, y)
y += 12

# ── Follow-up instructions ───────────────────────────────────────────────────
text(page, 40, y, "FOLLOW-UP INSTRUCTIONS", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

followups = [
    "1.  Review with Dr. Anjali Mehta (Orthopaedics) after 2 weeks — 27-March-2024.",
    "2.  Suture removal on Day 14 post-surgery at nearest surgical OPD.",
    "3.  Non-weight bearing on right leg for 6 weeks. Use crutches as instructed.",
    "4.  Physiotherapy to begin from Day 10 post-op (ROM exercises, quad strengthening).",
    "5.  Diabetes follow-up with Dr. Ravi Kulkarni (Endocrinology) within 1 month.",
    "6.  Repeat HbA1c and fasting glucose after 3 months.",
    "7.  Report immediately to ER if: fever >101°F, wound discharge, chest pain, or SOB.",
    "8.  MLC follow-up: Patient to appear before MACT as required. Case No. MLC/2024/0843.",
]
for line in followups:
    text(page, 44, y, line, size=8)
    y += 12
hline(page, y)
y += 12

# ── Consent & Signature section ──────────────────────────────────────────────
text(page, 40, y, "CONSENT & AUTHORIZATION", size=9, bold=True, color=(0.48,0.17,0.17))
y += 14
hline(page, y, color=(0.48,0.17,0.17), width=1)
y += 10

text(page, 40, y,
     "Informed written consent obtained for surgical procedure on 13-March-2024.",
     size=8)
y += 12
text(page, 40, y,
     "Consent form signed by: Patient (Mr. Rajesh Kumar Sharma) and Witness (Mrs. Sunita Sharma — Wife).",
     size=8)
y += 12
text(page, 40, y,
     "Anesthesia consent obtained. Patient educated about procedure risks and alternatives.",
     size=8)
y += 20

# Signature boxes
for sx, label, name in [
    (40,  "Consultant Surgeon",   "Dr. Anjali Mehta"),
    (200, "Resident Physician",   "Dr. Priya Desai"),
    (370, "Patient / Guardian",   "Mr. Rajesh K. Sharma"),
]:
    page.draw_rect(fitz.Rect(sx, y, sx+140, y+28), color=(0.7,0.7,0.7), width=0.5)
    text(page, sx+5, y+12, "Signature: ____________", size=7, color=(0.4,0.4,0.4))
    text(page, sx+5, y+22, label, size=7, bold=True)
    text(page, sx+5, y+32, name, size=7, color=(0.4,0.4,0.4))
y += 45

hline(page, y)
y += 10

# ── MLC Notice ───────────────────────────────────────────────────────────────
rect_fill(page, 40, y, 555, y+30, (1.0, 0.97, 0.93))
page.draw_rect(fitz.Rect(40, y, 555, y+30), color=(0.9, 0.6, 0.3), width=0.7)
text(page, 48, y+10, "MLC NOTICE:", size=8, bold=True, color=(0.8, 0.4, 0.0))
text(page, 130, y+10,
     "This is a Medico-Legal Case. MLC No: MLC/2024/0843. Police informed as per protocol.",
     size=8, color=(0.5, 0.3, 0.0))
text(page, 130, y+22,
     "Patient/Guardian advised to retain this document for insurance and legal proceedings.",
     size=7.5, color=(0.5, 0.3, 0.0))
y += 40

# ── Footer ───────────────────────────────────────────────────────────────────
rect_fill(page, 0, 800, 595, 842, (0.96, 0.93, 0.91))
hline(page, 800, width=0.5, color=(0.48,0.17,0.17))
text(page, 40,  815, "City General Hospital & Research Centre — Confidential Medical Record", size=7, color=(0.5,0.5,0.5))
text(page, 40,  827, "Generated: 20-March-2024 15:42 IST  |  For clinical use only. Not valid without authorized signature.", size=7, color=(0.5,0.5,0.5))
text(page, 490, 815, "Page 1 of 1", size=7, color=(0.5,0.5,0.5))

# ── Save ─────────────────────────────────────────────────────────────────────
doc.save(OUTPUT)
doc.close()
print(f"✅  Created: {OUTPUT}")
print(f"    Size   : {os.path.getsize(OUTPUT):,} bytes")

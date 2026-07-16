"""Quick end-to-end test of the 4-agent workflow."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medcompliance.utils.pdf_utils import extract_pdf_text
from medcompliance.agents.workflow import run_compliance_workflow

# Use existing sample PDF
PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "sample_case_dummy.pdf")

print("=== MedComply AI — End-to-End Test ===\n")

if os.path.exists(PDF_PATH):
    text = extract_pdf_text(PDF_PATH)
    print(f"PDF loaded: {len(text)} chars\n")
else:
    # Dummy text if PDF not found
    text = """
    HOSPITAL DISCHARGE SUMMARY
    Patient: Rahul Sharma, Age: 34, Gender: Male
    Hospital: City General Hospital, Dr. A. Mehta
    Admission: 2024-03-12, Discharge: 2024-03-20
    Diagnosis: Fracture of Right Femur, Head Injury
    Treatment: ORIF Surgery, Physiotherapy
    Medicines: Gabapentin 300mg, Analgesics
    """
    print("Using dummy text (sample PDF not found)\n")

result = run_compliance_workflow(text, "sample_case_dummy.pdf")

print("\n=== RESULTS ===")
print(f"Compliance Score : {result['compliance_score']}/100")
print(f"Risk Level       : {result['risk_level']}")
print(f"Audit Verdict    : {result['audit_verdict']}")
print(f"Violations       : {len(result['violations'])}")
print(f"Patient          : {result['patient_name']}")
print(f"Hospital         : {result['hospital_name']}")
print(f"\nExecutive Summary:")
print(result['executive_summary'][:300])
print("\n✅ Test complete!")

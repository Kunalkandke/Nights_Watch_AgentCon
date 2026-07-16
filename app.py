"""
MedComply AI — Healthcare Compliance & Governance Intelligence Agent
AgentCon 2026 | Built on LegalAI platform

Run: python medcompliance/app.py
Open: http://127.0.0.1:7000
"""

import os, sys, json, uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

# ── path setup so we can import from parent ──────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from medcompliance.agents.workflow import run_compliance_workflow
from medcompliance.utils.pdf_utils import extract_pdf_text

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "static"))

app.secret_key = "medcomply-agentcon-2026"
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    reports = session.get("reports", [])
    return render_template("dashboard.html", reports=reports)


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        return render_template("analyze.html")

    if "document" not in request.files or not request.files["document"].filename:
        return render_template("analyze.html", error="Please upload a medical document PDF.")

    pdf_file = request.files["document"]
    doc_name = pdf_file.filename
    save_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex[:8]}_{doc_name}")
    pdf_file.save(save_path)

    # Extract text
    text = extract_pdf_text(save_path)
    if not text.strip():
        text = f"[Document: {doc_name}] Sample medical record for compliance analysis."

    try:
        os.remove(save_path)
    except Exception:
        pass

    # Run 4-agent LangGraph workflow
    result = run_compliance_workflow(text, doc_name)

    # Store in session
    reports = session.get("reports", [])
    report_id = uuid.uuid4().hex[:8]
    reports.insert(0, {
        "id":         report_id,
        "doc_name":   doc_name,
        "score":      result.get("compliance_score", 0),
        "risk":       result.get("risk_level", "Unknown"),
        "timestamp":  result.get("timestamp", ""),
    })
    session["reports"] = reports[:10]
    session.modified = True

    return render_template("report.html", result=result, doc_name=doc_name, report_id=report_id)


@app.route("/report/<report_id>")
def report_detail(report_id):
    # For re-viewing (would need DB in prod — for MVP use demo data)
    return render_template("report.html",
                           result=session.get(f"report_{report_id}", {}),
                           doc_name="Report",
                           report_id=report_id)


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """AJAX endpoint — runs workflow, returns JSON."""
    data = request.get_json() or {}
    text = data.get("text", "")
    doc_name = data.get("doc_name", "document.pdf")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = run_compliance_workflow(text, doc_name)
    return jsonify(result)


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  🏥  MedComply AI — AgentCon 2026")
    print("=" * 55)
    print("  Dashboard  →  http://127.0.0.1:7000/dashboard")
    print("  Analyze    →  http://127.0.0.1:7000/analyze")
    print("=" * 55 + "\n")
    app.run(debug=True, port=7000)

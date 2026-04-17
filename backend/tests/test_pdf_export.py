import os
from backend import pdf_exporter
from fastapi.testclient import TestClient
from backend.main import app


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_export_pdf_function():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    tailored = load(os.path.join(root, "sample_data", "sample_tailored.txt"))
    pdf = pdf_exporter.export_pdf(tailored)
    assert isinstance(pdf, (bytes, bytearray))
    assert len(pdf) > 0
    assert pdf[:4] == b"%PDF"


def test_export_pdf_endpoint():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    tailored = load(os.path.join(root, "sample_data", "sample_tailored.txt"))
    client = TestClient(app)
    resp = client.post("/api/export/pdf", json={"text": tailored})
    assert resp.status_code == 200
    assert resp.headers.get("content-type") == "application/pdf"

import os
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_tailor_endpoint():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    resume = load(os.path.join(root, "sample_data", "sample_resume.txt"))
    job = load(os.path.join(root, "sample_data", "sample_job.txt"))

    resp = client.post("/api/tailor", json={"resume": resume, "job": job})
    assert resp.status_code == 200
    data = resp.json()
    assert "tailored_text" in data
    assert "TAILORED_FOR" in data["tailored_text"]

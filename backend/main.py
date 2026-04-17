from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from backend.models import TailorRequest, TailorResponse, PdfRequest
from backend import tailor_engine, pdf_exporter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/tailor", response_model=TailorResponse)
def tailor(req: TailorRequest):
    text = tailor_engine.generate_tailored_resume(req.resume, req.job)
    return {"tailored_text": text}


@app.post("/api/export/pdf")
def export_pdf(req: PdfRequest):
    pdf_bytes = pdf_exporter.export_pdf(req.text)
    return Response(content=pdf_bytes, media_type="application/pdf")

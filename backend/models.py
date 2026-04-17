from pydantic import BaseModel


class TailorRequest(BaseModel):
    resume: str
    job: str


class TailorResponse(BaseModel):
    tailored_text: str


class PdfRequest(BaseModel):
    text: str

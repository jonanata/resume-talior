from io import BytesIO
import os
import unicodedata
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_unicode_font() -> str:
    candidates = [
        # common DejaVu paths (Linux)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/local/share/fonts/DejaVuSans.ttf",
        # common Windows paths
        "C:\\Windows\\Fonts\\DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        # macOS paths
        "/Library/Fonts/DejaVuSans.ttf",
        "/System/Library/Fonts/Arial.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont("DejaVuSans", p))
                return "DejaVuSans"
            except Exception:
                continue
    return "Helvetica"


def _safe_text_for_font(text: str, font_name: str) -> str:
    if font_name == "Helvetica":
        return text.encode("latin-1", errors="replace").decode("latin-1")
    return text


def export_pdf(text: str) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter

    font_name = _register_unicode_font()
    font_size = 12
    c.setFont(font_name, font_size)

    max_width = width - 100
    y = height - 50

    from reportlab.pdfbase.pdfmetrics import stringWidth

    for raw_line in text.splitlines():
        line = _safe_text_for_font(raw_line, font_name)
        words = line.split(" ")
        cur = ""
        for w in words:
            test = (cur + " " + w).strip() if cur else w
            if stringWidth(test, font_name, font_size) <= max_width:
                cur = test
            else:
                c.drawString(50, y, cur)
                y -= font_size + 2
                if y < 50:
                    c.showPage()
                    c.setFont(font_name, font_size)
                    y = height - 50
                cur = w
        if cur:
            c.drawString(50, y, cur)
            y -= font_size + 2
            if y < 50:
                c.showPage()
                c.setFont(font_name, font_size)
                y = height - 50

    c.save()
    pdf = buf.getvalue()
    buf.close()
    return pdf

import React from "react";
import { exportPdf } from "./api";

export default function DownloadPdfButton({ text }) {
  const handleDownload = async () => {
    const blob = await exportPdf(text);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "tailored.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return <button data-testid="download-pdf-button" onClick={handleDownload}>Download PDF</button>;
}

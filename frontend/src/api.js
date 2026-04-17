export async function tailorResume(resume, job) {
  const resp = await fetch("http://localhost:8000/api/tailor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume, job }),
  });
  return resp.json();
}

export async function exportPdf(text) {
  const resp = await fetch("http://localhost:8000/api/export/pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const blob = await resp.blob();
  return blob;
}

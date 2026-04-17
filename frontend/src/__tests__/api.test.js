import { tailorResume, exportPdf } from "../api";

global.fetch = jest.fn();

afterEach(() => {
  fetch.mockClear();
});

test("tailorResume calls /api/tailor", async () => {
  fetch.mockResolvedValueOnce({ json: async () => ({ tailored_text: "ok" }) });
  const resume = "r";
  const job = "j";
  await tailorResume(resume, job);
  expect(fetch).toHaveBeenCalledWith("http://localhost:8000/api/tailor", expect.objectContaining({ method: "POST" }));
});

test("exportPdf calls /api/export/pdf", async () => {
  fetch.mockResolvedValueOnce({ blob: async () => new Blob(["pdf"] , { type: 'application/pdf' }) });
  await exportPdf("t");
  expect(fetch).toHaveBeenCalledWith("http://localhost:8000/api/export/pdf", expect.objectContaining({ method: "POST" }));
});

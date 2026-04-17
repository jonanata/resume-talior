import React, { useState } from "react";
import { tailorResume } from "./api";
import ResultView from "./ResultView";
import DownloadPdfButton from "./DownloadPdfButton";

export default function TailorForm() {
  const [resume, setResume] = useState("");
  const [job, setJob] = useState("");
  const [result, setResult] = useState("");

  const handleTailor = async () => {
    const data = await tailorResume(resume, job);
    setResult(data.tailored_text || "");
  };

  return (
    <div>
      <textarea data-testid="resume-input" value={resume} onChange={(e) => setResume(e.target.value)} />
      <textarea data-testid="job-input" value={job} onChange={(e) => setJob(e.target.value)} />
      <button data-testid="tailor-button" onClick={handleTailor}>Tailor</button>
      <ResultView text={result} />
      <DownloadPdfButton text={result} />
    </div>
  );
}

import React from "react";
import { render, fireEvent } from "@testing-library/react";
import TailorForm from "../TailorForm";
import * as api from "../api";
import fs from "fs";
import path from "path";

test("calls tailorResume with file contents", async () => {
  const root = path.resolve(__dirname, "..", "..", "..");
  const resume = fs.readFileSync(path.join(root, "sample_data", "sample_resume.txt"), "utf8");
  const job = fs.readFileSync(path.join(root, "sample_data", "sample_job.txt"), "utf8");

  const mock = jest.spyOn(api, "tailorResume").mockResolvedValue({ tailored_text: "ok" });

  const { getByTestId } = render(<TailorForm />);
  const r = getByTestId("resume-input");
  const j = getByTestId("job-input");
  const b = getByTestId("tailor-button");

  fireEvent.change(r, { target: { value: resume } });
  fireEvent.change(j, { target: { value: job } });
  fireEvent.click(b);

  expect(mock).toHaveBeenCalledWith(resume, job);
  mock.mockRestore();
});

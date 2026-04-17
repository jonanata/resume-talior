import React from "react";
import { render } from "@testing-library/react";
import ResultView from "../ResultView";
import fs from "fs";
import path from "path";

test("displays tailored text", () => {
  const root = path.resolve(__dirname, "..", "..", "..");
  const tailored = fs.readFileSync(path.join(root, "sample_data", "sample_tailored.txt"), "utf8");
  const { getByTestId } = render(<ResultView text={tailored} />);
  expect(getByTestId("result-container").textContent).toContain(tailored.slice(0, 20));
});

# dev.md — AI‑Native Full Automation Development Workflow  
React UI + FastAPI + Auto‑Tests + Auto‑Commit + Auto‑Review

## 1. Project Overview  
This project is a fully autonomous full‑stack Resume Tailor App.  
The system must:

- Provide a React UI for resume + job description  
- Provide a FastAPI backend for tailoring + PDF export  
- Auto‑run backend tests  
- Auto‑run UI tests  
- Auto‑save logs  
- Auto‑commit + push to GitHub when tests pass  
- Auto‑trigger Copilot code review  
- Require zero manual test execution  
- Use this dev.md file as the single source of truth  

GitHub Copilot reads this file and generates/updates all code.

## 2. Repository Structure  
resume-tailor/  
sample_data/  
backend/  
main.py  
models.py  
tailor_engine.py  
pdf_exporter.py  
tests/  
requirements.txt  
frontend/  
package.json  
src/  
TailorForm.jsx  
ResultView.jsx  
DownloadPdfButton.jsx  
api.js  
__tests__/  
public/  
auto_runner.py  
test_results/  
dev.md

## 3. Backend (FastAPI)  
@copilot:  
Create backend files:

backend/main.py  
backend/models.py  
backend/tailor_engine.py  
backend/pdf_exporter.py  
backend/tests/  
backend/requirements.txt  

Requirements:  
FastAPI app  
POST /api/tailor → returns tailored resume JSON  
POST /api/export/pdf → returns PDF bytes  
Use Pydantic models  
Use tailor_engine.generate_tailored_resume()  
Use pdf_exporter.export_pdf()  
Enable CORS for React

## 4. Frontend (React)  
@copilot:  
Create React app in ./frontend with:

Components:  
TailorForm.jsx  
ResultView.jsx  
DownloadPdfButton.jsx  

API:  
api.js with tailorResume(resume, job) and exportPdf(tailoredResume)

UI Flow:  
User pastes resume + job description  
Clicks “Tailor”  
Shows tailored result  
Clicks “Download PDF”

## 4.1 UI Structure (IMPORTANT FOR TESTS)  
@copilot:  
Use these exact test IDs in the React UI:

resume-input → textarea for resume  
job-input → textarea for job description  
tailor-button → button to trigger tailoring  
result-container → div showing tailored resume  
download-pdf-button → button to download PDF  

TailorForm.jsx must contain:  
<textarea data-testid="resume-input">  
<textarea data-testid="job-input">  
<button data-testid="tailor-button">Tailor</button>

ResultView.jsx must contain:  
<div data-testid="result-container">…</div>

DownloadPdfButton.jsx must contain:  
<button data-testid="download-pdf-button">Download PDF</button>

These IDs must be used consistently so UI tests can target them.

## 5. Backend Tests (pytest)

### 5.1 Use my sample_data folder  
@copilot:  
Use my existing sample data files located in ./sample_data/ for all backend tests.

Files:  
./sample_data/sample_resume.txt  
./sample_data/sample_job.txt  
./sample_data/sample_tailored.txt  

Do NOT generate new sample files.  
Always load the files from ./sample_data/.

### 5.2 Backend Test Behavior  
@copilot:

test_tailor_endpoint.py:  
- load sample_resume.txt  
- load sample_job.txt  
- POST /api/tailor with these contents  
- assert 200  
- assert JSON structure  
- assert returned text contains expected tailored markers  

test_pdf_export.py:  
- load sample_tailored.txt  
- call export_pdf() with this text  
- assert PDF bytes length > 0  
- POST /api/export/pdf with this text  
- assert 200  
- assert response is application/pdf  

## 6. UI Tests (Jest + React Testing Library)

### 6.1 Use my sample_data folder  
@copilot:  
Use my existing sample data files located in ./sample_data/ for all UI tests.

Files:  
./sample_data/sample_resume.txt  
./sample_data/sample_job.txt  
./sample_data/sample_tailored.txt  

Do NOT generate new sample files.  
Always load the files from ./sample_data/.

### 6.2 UI Test Behavior  
@copilot:

TailorForm.test.jsx:  
- load sample_resume.txt  
- load sample_job.txt  
- fill resume-input with the file contents  
- fill job-input with the file contents  
- click tailor-button  
- assert tailorResume() was called with the exact file contents  

ResultView.test.jsx:  
- load sample_tailored.txt  
- render component with this text  
- assert result-container displays the text  

api.test.js:  
- mock fetch  
- assert tailorResume() calls /api/tailor with the file contents  
- assert exportPdf() calls /api/export/pdf  

All tests must use getByTestId() selectors.

## 7. Full Automation Engine (auto_runner.py)  
@copilot:  
Create auto_runner.py with:

1. Watch these directories:  
backend/  
frontend/src/  
backend/tests/  
frontend/src/__tests__/  
tailor_engine/

2. On ANY file change:  
Start backend (uvicorn backend.main:app --reload)  
Start frontend (npm start)  
Wait until:  
http://localhost:8000 responds  
http://localhost:3000 responds  

3. Run backend tests:  
pytest -q  
Save to test_results/backend_<timestamp>.txt  

4. Run UI tests:  
npm test -- --watchAll=false  
Save to test_results/ui_<timestamp>.txt  

5. If ALL tests pass:  
git add .  
Generate commit message:  
“@copilot: Summarize latest changes and test results for commit.”  
git commit -m “<AI message>”  
git push  

6. If ANY test fails:  
print “Tests failed — commit skipped.”

7. Shut down both servers  

8. Append summary to test_results/summary.log  

9. Print:  
“@copilot: Review latest test logs and propose fixes.”

## 8. Log Parsing Rules  
@copilot:  
Update auto_runner.py tests_passed() to treat any of:  
FAILED  
ERROR  
Traceback  
TypeError  
ReferenceError  
Unhandled  
as failure.

## 9. AI Code Review Trigger  
@copilot:  
After every automated test cycle, review the latest test_results/*.txt files.  
Identify:  
failing backend tests  
failing UI tests  
root cause analysis  
recommended fixes  
missing test cases  
refactoring opportunities

## 10. Developer Workflow (Zero Manual Testing)  
Once everything is generated:

Start the autonomous system:  
python auto_runner.py

Then:  
You edit any file  
You save  
The system automatically:

Start backend  
Start frontend  
Run backend tests  
Run UI tests  
Save logs  
Auto‑commit if clean  
Auto‑push if clean  
Shut down servers  
Trigger Copilot review  

You never manually run tests again.

## 11. Release Automation (Optional)  
@copilot:  
If tests pass AND commit is created:  
auto‑tag version  
auto‑generate release notes  
auto‑push tag

## 12. End of File  
This dev.md file is the single source of truth.  
GitHub Copilot reads it and generates/updates the entire system.  


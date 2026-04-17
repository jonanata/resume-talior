import os
import time
import subprocess
import threading
import requests
from datetime import datetime
import shutil
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_DIR = os.path.join(ROOT, "test_results")
os.makedirs(TEST_DIR, exist_ok=True)


def timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def run_cmd(cmd, cwd=None):
    p = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def wait_for(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def tests_passed(text):
    bad = ["FAILED", "ERROR", "Traceback", "TypeError", "ReferenceError", "Unhandled"]
    for b in bad:
        if b in text:
            return False
    return True


def run_cycle():
    # start backend (use `uvicorn` if available, otherwise run as module)
    if shutil.which("uvicorn"):
        backend_cmd = ["uvicorn", "backend.main:app", "--reload"]
    else:
        backend_cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"]
    try:
        backend_proc = subprocess.Popen(backend_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        print("Unable to start backend: uvicorn not found and python -m uvicorn failed.")
        raise

    # start frontend only if npm is available
    if shutil.which("npm"):
        try:
            frontend_proc = subprocess.Popen(["npm", "start"], cwd=os.path.join(ROOT, "frontend"), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except FileNotFoundError:
            frontend_proc = None
    else:
        print("npm not found on PATH — skipping frontend startup and UI tests")
        frontend_proc = None

    try:
        if not wait_for("http://localhost:8000", timeout=30):
            print("Backend did not start in time")

        if frontend_proc is not None:
            if not wait_for("http://localhost:3000", timeout=30):
                print("Frontend did not start in time")

        # run backend tests
        # ensure tests can import `backend` by setting PYTHONPATH
        env_pythonpath = os.environ.get("PYTHONPATH", "")
        if ROOT not in env_pythonpath.split(os.pathsep):
            os.environ["PYTHONPATH"] = ROOT + (os.pathsep + env_pythonpath if env_pythonpath else "")
        rc, out = run_cmd("pytest -q", cwd=ROOT)
        fname = os.path.join(TEST_DIR, f"backend_{timestamp()}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(out)

        backend_ok = tests_passed(out)

        # run UI tests
        ui_ok = True
        if frontend_proc is not None:
            rc2, out2 = run_cmd("npm test -- --watchAll=false", cwd=os.path.join(ROOT, "frontend"))
            fname2 = os.path.join(TEST_DIR, f"ui_{timestamp()}.txt")
            with open(fname2, "w", encoding="utf-8") as f:
                f.write(out2)

            ui_ok = tests_passed(out2)

        summary = f"backend_ok={backend_ok} ui_ok={ui_ok}"
        with open(os.path.join(TEST_DIR, "summary.log"), "a", encoding="utf-8") as f:
            f.write(f"{timestamp()} {summary}\n")

        if backend_ok and ui_ok:
            # commit and push
            run_cmd("git add .", cwd=ROOT)
            commit_msg = "@copilot: Summarize latest changes and test results for commit."
            run_cmd(f"git commit -m \"{commit_msg}\"", cwd=ROOT)
            run_cmd("git push", cwd=ROOT)
            print("@copilot: Review latest test logs and propose fixes.")
        else:
            print("Tests failed — commit skipped.")

    finally:
        try:
            backend_proc.terminate()
        except Exception:
            pass
        try:
            if frontend_proc:
                frontend_proc.terminate()
        except Exception:
            pass


if __name__ == "__main__":
    print("Starting auto_runner (single cycle). Press Ctrl-C to exit.")
    run_cycle()

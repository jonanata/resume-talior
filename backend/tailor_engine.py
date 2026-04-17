def generate_tailored_resume(resume_text: str, job_text: str) -> str:
    # Simple deterministic tailoring: include a header and sprinkle keywords
    header = "TAILORED_FOR: " + (job_text.splitlines()[0] if job_text.strip() else "unknown job")
    # extract simple keywords
    words = [w.strip('.,()[]') for w in job_text.split()]
    keywords = [w for w in words if len(w) > 4]
    keywords = list(dict.fromkeys(keywords))[:10]
    footer = "\n\n-- Keywords: " + ", ".join(keywords)
    return header + "\n\n" + resume_text + footer

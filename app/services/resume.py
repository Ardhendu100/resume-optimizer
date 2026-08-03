from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RESUME_DIR = BASE_DIR / "resume_template"
RESUME_FILE = RESUME_DIR / "resume.tex"


def load_resume() -> str:
    """
    Read the original resume.tex file.
    """
    return RESUME_FILE.read_text(encoding="utf-8")
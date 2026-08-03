from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class CompileResult:
    success: bool
    pdf_path: Path
    stdout: str
    stderr: str
    returncode: int
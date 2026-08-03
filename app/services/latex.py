from pathlib import Path
import shutil
import subprocess

from app.schemas.compile import CompileResult


def compile_resume(
    workspace_dir: Path,
    output_dir: Path,
) -> CompileResult:

    if shutil.which("pdflatex") is None:
        return CompileResult(
            success=False,
            pdf_path=output_dir / "resume.pdf",
            stdout="",
            stderr="pdflatex is not installed.",
            returncode=-1,
        )

    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={output_dir}",
        "resume.tex",
    ]

    result = subprocess.run(
        command,
        cwd=workspace_dir,
        capture_output=True,
        text=True,
    )

    return CompileResult(
        success=result.returncode == 0,
        pdf_path=output_dir / "resume.pdf",
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
    )
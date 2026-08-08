from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.workspace import Workspace, TEMP_ROOT, GENERATED_ROOT
from app.services.latex import compile_resume
from app.services.ai import optimize_resume


router = APIRouter(
    prefix="/api",
    tags=["Analyze"]
)


# Temporary workspace storage
# Later we can replace this with Redis/database
workspaces = {}


class AnalyzeRequest(BaseModel):
    """Request body for the analyze endpoint.

    The job description is currently unused by the backend but is
    required by the frontend to send a JSON payload.  Keeping the
    model makes the API explicit and allows future extensions.
    """

    job_description: str


@router.post("/analyze")
async def analyze_resume(request: AnalyzeRequest):

    # Create isolated workspace
    workspace = Workspace()

    # Copy resume.tex and resume.cls
    workspace.prepare()

    # Compile original resume first (optional, but keeps existing flow)
    original_compile = compile_resume(
        workspace_dir=workspace.temp_dir,
        output_dir=workspace.output_dir,
    )

    # Read original tex
    original_tex = workspace.tex_file.read_text(encoding="utf-8")

    # Ask Gemini for optimization
    ai_result = optimize_resume(
        job_description=request.job_description,
        original_tex=original_tex,
    )

    # Write optimized tex to workspace
    optimized_tex_path = workspace.tex_file
    optimized_tex_path.write_text(ai_result["optimized_tex"], encoding="utf-8")

    # Compile optimized resume
    compile_result = compile_resume(
        workspace_dir=workspace.temp_dir,
        output_dir=workspace.output_dir,
    )


    # Store workspace for future requests
    workspaces[workspace.workspace_id] = workspace


    return {
        "success": compile_result.success,
        "workspace_id": workspace.workspace_id,
        "pdf_exists": compile_result.pdf_path.exists(),
        "pdf_path": str(compile_result.pdf_path),
        "return_code": compile_result.returncode,
        "stdout": compile_result.stdout[-500:],
        "stderr": compile_result.stderr[-500:],
        "ats_score": ai_result["ats_score"],
        "matched_keywords": ai_result["matched_keywords"],
        "missing_keywords": ai_result["missing_keywords"],
        "suggestions": ai_result["suggestions"],
    }



@router.get("/pdf/{workspace_id}")
def preview_pdf(workspace_id: str):

    workspace = workspaces.get(workspace_id)

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )


    if not workspace.pdf_file.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF not generated"
        )


    return FileResponse(
        path=workspace.pdf_file,
        media_type="application/pdf"
    )



@router.get("/download/pdf/{workspace_id}")
def download_pdf(workspace_id: str):

    workspace = workspaces.get(workspace_id)

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )


    if not workspace.pdf_file.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF not generated"
        )


    return FileResponse(
        path=workspace.pdf_file,
        media_type="application/pdf",
        filename="optimized_resume.pdf"
    )



@router.get("/download/tex/{workspace_id}")
def download_tex(workspace_id: str):

    workspace = workspaces.get(workspace_id)

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )


    if not workspace.tex_file.exists():
        raise HTTPException(
            status_code=404,
            detail="TEX file not found"
        )


    return FileResponse(
        path=workspace.tex_file,
        media_type="application/x-tex",
        filename="resume.tex"
    )

@router.post("/reset")
def reset_workspace():
    """Clear all temporary and generated files and reset in‑memory state.

    This endpoint is intended for the UI reset button.  It removes the
    contents of the ``temp`` and ``generated`` directories and clears the
    ``workspaces`` dictionary.
    """
    import shutil

    # Remove temp and generated directories
    shutil.rmtree(TEMP_ROOT, ignore_errors=True)
    shutil.rmtree(GENERATED_ROOT, ignore_errors=True)
    # Re‑create root directories
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    # Clear in‑memory workspaces
    workspaces.clear()
    return {"success": True}
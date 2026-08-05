from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.workspace import Workspace
from app.services.latex import compile_resume


router = APIRouter(
    prefix="/api",
    tags=["Analyze"]
)


# Temporary workspace storage
# Later we can replace this with Redis/database
workspaces = {}


@router.post("/analyze")
async def analyze_resume():

    # Create isolated workspace
    workspace = Workspace()

    # Copy resume.tex and resume.cls
    workspace.prepare()

    # Compile LaTeX
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
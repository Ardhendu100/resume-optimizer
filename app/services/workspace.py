from pathlib import Path
import shutil
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATE_DIR = BASE_DIR / "resume_template"
TEMP_ROOT = BASE_DIR / "temp"
GENERATED_ROOT = BASE_DIR / "generated"


class Workspace:
    def __init__(self):
        self.workspace_id = str(uuid.uuid4())

        self.temp_dir = TEMP_ROOT / self.workspace_id
        self.output_dir = GENERATED_ROOT / self.workspace_id

    def prepare(self):
        """
        Create isolated workspace.
        """

        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(
            TEMPLATE_DIR / "resume.tex",
            self.temp_dir / "resume.tex",
        )

        shutil.copy2(
            TEMPLATE_DIR / "resume.cls",
            self.temp_dir / "resume.cls",
        )

    @property
    def tex_file(self):
        return self.temp_dir / "resume.tex"

    @property
    def pdf_file(self):
        return self.output_dir / "resume.pdf"

    def cleanup(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)
"""Gemini integration for ATS analysis and resume optimization."""

from typing import List

from pydantic import BaseModel
from google import genai

from app.config import settings


# -------------------------------------------------------------------
# Response schema
# -------------------------------------------------------------------

class ATSResult(BaseModel):
    ats_score: int
    matched_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]
    optimized_tex: str


# -------------------------------------------------------------------
# Gemini client
# -------------------------------------------------------------------

client = None


def _initialize_gemini() -> None:
    """Initialize the Gemini client."""

    global client

    if client is None:
        api_key = settings.GEMINI_API_KEY

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable not set"
            )

        client = genai.Client(api_key=api_key)


# -------------------------------------------------------------------
# Resume optimization
# -------------------------------------------------------------------

def optimize_resume(
    job_description: str,
    original_tex: str,
) -> dict:
    """Analyze and optimize a LaTeX resume using Gemini."""

    _initialize_gemini()

    system_prompt = """
You are an expert ATS resume reviewer and resume optimization assistant.

Your task is to analyze the provided job description against the provided
LaTeX resume.

Return the following information:

1. ats_score:
   - Integer from 0 to 100.
   - Represents how well the resume matches the job description.

2. matched_keywords:
   - Important skills, technologies, tools, concepts, and keywords
     present in both the job description and resume.

3. missing_keywords:
   - Important keywords from the job description that are missing
     or insufficiently represented in the resume.

4. suggestions:
   - Specific actionable suggestions to improve ATS compatibility
     and alignment with the job description.

5. optimized_tex:
   - The complete optimized LaTeX resume.
   - Preserve the existing resume structure and formatting.
   - Do NOT invent experience.
   - Do NOT invent companies.
   - Do NOT invent projects.
   - Do NOT invent education.
   - Do NOT invent certifications.
   - Do NOT invent achievements.
   - Only improve wording, keyword alignment, ordering, and presentation
     using information already present in the original resume.
   - The resulting LaTeX must remain valid and compile using the existing
     resume.cls.

IMPORTANT:
Return only the structured response requested by the schema.
Do not wrap the response in Markdown.
"""

    user_prompt = (
        f"{system_prompt}\n\n"
        f"JOB DESCRIPTION:\n"
        f"{job_description}\n\n"
        f"ORIGINAL RESUME LATEX:\n"
        f"{original_tex}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config={
                "temperature": 0.2,
                "top_p": 1,
                "top_k": 32,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json",
                "response_schema": ATSResult,
            },
        )

    except Exception as exc:
        raise RuntimeError(
            f"Gemini API request failed: {exc}"
        ) from exc

    # ----------------------------------------------------------------
    # Parse structured response
    # ----------------------------------------------------------------

    try:
        result = ATSResult.model_validate_json(response.text)
    except Exception as exc:
        raise RuntimeError(
            "Gemini returned an invalid structured response"
        ) from exc

    # ----------------------------------------------------------------
    # Validate ATS score
    # ----------------------------------------------------------------

    if not 0 <= result.ats_score <= 100:
        raise RuntimeError(
            f"Invalid ATS score returned by Gemini: "
            f"{result.ats_score}"
        )

    return result.model_dump()
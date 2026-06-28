import re
import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ─── PROMPT TEMPLATE ──────────────────────────────────────────────────────────
load_dotenv()

LLM_PROMPT = """You are an expert ATS (Applicant Tracking System) Resume Analyzer.

Analyze the resume below against the given job role. Return ONLY a valid JSON object with no extra text, markdown, or explanation. The JSON must exactly follow this schema:

{{
  "ats_score": <integer 0-100>,
  "matched_skills": [<list of strings>],
  "missing_keywords": [<list of strings>],
  "resume_improvements": [<list of strings>],
  "section_wise_suggestions": {{
    "Summary": "<string>",
    "Skills": "<string>",
    "Experience": "<string>",
    "Projects": "<string>"
  }},
  "final_verdict": "<string, 2-3 sentences>"
}}

Resume:
{resume}

Job Role: {job_role}

Return ONLY the JSON object."""

def extract_text_from_file(uploaded_file) -> str:
    """Extract text from PDF or DOCX file."""
    text = ""
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    try:
        if ext == '.pdf':
            from PyPDF2 import PdfReader
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif ext in ['.docx', '.doc']:
            import docx
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = uploaded_file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[Extractor Error] {e}")
    return text.strip()


def analyze_resume_with_ai(resume_text: str, target_role: str = '') -> dict:
    """
    Uses huggingface_hub InferenceClient with chat_completion
    to analyze the resume and return structured data.
    """
    target_role = target_role.strip() or "General Role"
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN", "").strip('"').strip("'")

    try:
        client = InferenceClient(token=token)

        prompt = LLM_PROMPT.format(
            resume=resume_text[:3000],
            job_role=target_role,
        )

        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model="Qwen/Qwen2.5-72B-Instruct",
            max_tokens=1500,
            temperature=0.4,
        )

        content = response.choices[0].message.content.strip()

        # Strip markdown code blocks if present
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'^```\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        content = content.strip()

        # Parse JSON
        parsed = json.loads(content)

        section_suggestions = parsed.get("section_wise_suggestions", {})

        return {
            "ats_score": int(parsed.get("ats_score", 0)),
            "overall_summary": parsed.get("final_verdict", "Analysis complete."),
            "section_feedback": {
                "contact_information": {"score": 100, "feedback": "", "missing": []},
                "education":           {"score": 100, "feedback": "", "missing": []},
                "experience":          {"score": int(parsed.get("ats_score", 0)), "feedback": section_suggestions.get("Experience", ""), "missing": []},
                "skills":              {"score": int(parsed.get("ats_score", 0)), "feedback": section_suggestions.get("Skills", ""), "missing": []},
                "projects":            {"score": int(parsed.get("ats_score", 0)), "feedback": section_suggestions.get("Projects", ""), "missing": []},
                "summary":             {"score": int(parsed.get("ats_score", 0)), "feedback": section_suggestions.get("Summary", ""), "missing": []},
            },
            "keywords_present":  parsed.get("matched_skills", []),
            "keywords_missing":  parsed.get("missing_keywords", []),
            "improvements":      parsed.get("resume_improvements", []),
            "suggestions":       [],
            "strengths":         [],
            "formatting_tips":   [],
        }

    except Exception as e:
        import traceback
        print(f"[LLM Error Details]:")
        traceback.print_exc()
        return {
            "ats_score": 0,
            "overall_summary": "Analysis failed due to a server error. Please try again.",
            "section_feedback": {},
            "keywords_present": [],
            "keywords_missing": [],
            "improvements": [],
            "suggestions": ["Please re-upload your resume or try again later."],
            "strengths": [],
            "formatting_tips": [],
        }

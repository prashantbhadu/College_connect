"""
Utility functions for resume parsing and AI analysis.
"""
import json
import io
from django.conf import settings


def parse_pdf(file) -> str:
    """Extract text from a PDF file object."""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or '')
        return '\n'.join(text)
    except Exception as e:
        return f"[PDF parsing error: {str(e)}]"


def parse_docx(file) -> str:
    """Extract text from a DOCX file object."""
    try:
        import docx
        doc = docx.Document(file)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"[DOCX parsing error: {str(e)}]"


def extract_text_from_file(uploaded_file) -> str:
    """Dispatch to correct parser based on file extension."""
    name = uploaded_file.name.lower()
    if name.endswith('.pdf'):
        return parse_pdf(uploaded_file)
    elif name.endswith('.docx'):
        return parse_docx(uploaded_file)
    else:
        return "[Unsupported file type]"


ANALYSIS_PROMPT = """You are an expert resume analyst and ATS specialist. Analyze the following resume and return ONLY a valid JSON object with NO extra text, NO markdown, NO code blocks.

Target Role: {target_role}

Resume Text:
{resume_text}

Return this exact JSON structure:
{{
  "ats_score": <integer 0-100>,
  "overall_summary": "<2-3 sentence summary>",
  "section_feedback": {{
    "contact_information": {{"score": <0-100>, "feedback": "<text>", "missing": []}},
    "education": {{"score": <0-100>, "feedback": "<text>", "missing": []}},
    "experience": {{"score": <0-100>, "feedback": "<text>", "missing": []}},
    "skills": {{"score": <0-100>, "feedback": "<text>", "missing": []}},
    "projects": {{"score": <0-100>, "feedback": "<text>", "missing": []}}
  }},
  "keywords_missing": ["<keyword1>", "<keyword2>"],
  "keywords_present": ["<keyword1>", "<keyword2>"],
  "improvements": ["<improvement1>", "<improvement2>"],
  "suggestions": ["<suggestion1>", "<suggestion2>"],
  "strengths": ["<strength1>", "<strength2>"],
  "formatting_tips": ["<tip1>", "<tip2>"]
}}"""


def analyze_resume_with_ai(resume_text: str, target_role: str = '') -> dict:
    """
    Analyze resume text using OpenAI API.
    Falls back to a structured mock response if API key is not configured.
    """
    api_key = getattr(settings, 'OPENAI_API_KEY', '')

    if not api_key or api_key.startswith('sk-your'):
        return _mock_analysis(resume_text, target_role)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = ANALYSIS_PROMPT.format(
            target_role=target_role or 'Software Engineer',
            resume_text=resume_text[:8000]  # Limit context
        )

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You are an expert resume analyst. Always respond with valid JSON only.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        content = response.choices[0].message.content.strip()
        # Strip markdown code blocks if returned
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        return json.loads(content)

    except json.JSONDecodeError:
        return _mock_analysis(resume_text, target_role)
    except Exception as e:
        return {'error': str(e), **_mock_analysis(resume_text, target_role)}


def _mock_analysis(resume_text: str, target_role: str) -> dict:
    """Provides a realistic mock analysis when OpenAI is not configured."""
    word_count = len(resume_text.split())
    base_score = min(75, max(40, word_count // 10))

    return {
        "ats_score": base_score,
        "overall_summary": (
            f"This resume has been analyzed for a {target_role or 'general'} position. "
            "The document shows potential but has areas for improvement to better match ATS requirements. "
            "Consider adding more quantified achievements and industry-specific keywords."
        ),
        "section_feedback": {
            "contact_information": {
                "score": 85,
                "feedback": "Contact information is present. Ensure LinkedIn and GitHub URLs are included.",
                "missing": ["LinkedIn URL", "GitHub URL"]
            },
            "education": {
                "score": 80,
                "feedback": "Education section is well-structured. Include CGPA if above 7.5.",
                "missing": ["CGPA / GPA"]
            },
            "experience": {
                "score": 65,
                "feedback": "Experience section needs more quantified achievements. Use action verbs and metrics.",
                "missing": ["Quantified impact metrics", "Specific technologies used"]
            },
            "skills": {
                "score": 70,
                "feedback": "Skills section is present. Organize into categories (Languages, Frameworks, Tools).",
                "missing": ["Cloud platforms", "CI/CD tools"]
            },
            "projects": {
                "score": 75,
                "feedback": "Projects are listed. Add GitHub links and describe impact for each project.",
                "missing": ["GitHub links", "Live demo links", "Team size / role"]
            }
        },
        "keywords_missing": [
            f"{target_role or 'Software'} development",
            "Agile / Scrum",
            "REST APIs",
            "Version control (Git)",
            "Problem solving"
        ],
        "keywords_present": ["Python", "HTML", "CSS"],
        "improvements": [
            "Add more quantified achievements (e.g., 'Reduced load time by 40%')",
            "Include a professional summary at the top",
            "Use consistent formatting and bullet points",
            "Keep resume to 1 page for freshers / 2 pages for experienced"
        ],
        "suggestions": [
            f"Tailor your skills section to match {target_role or 'your target'} job descriptions",
            "Add certifications from Coursera, edX, or similar platforms",
            "Include open-source contributions if any",
            "Proofread for grammar and spelling errors"
        ],
        "strengths": [
            "Clear section headers",
            "Reverse chronological order used correctly"
        ],
        "formatting_tips": [
            "Use standard fonts (Arial, Calibri, Times New Roman) for ATS compatibility",
            "Avoid tables, columns, and graphics — ATS cannot parse them",
            "Save as PDF to preserve formatting",
            "Use standard section headings: Work Experience, Education, Skills, Projects"
        ]
    }

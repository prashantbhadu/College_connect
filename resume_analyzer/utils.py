<<<<<<< HEAD
import re
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# ─── PYDANTIC SCHEMAS FOR STRUCTURED OUTPUT ───────────────────────────────────
load_dotenv()
class SectionSuggestions(BaseModel):
    Summary: str = Field(description="Actionable suggestion for the Summary section")
    Skills: str = Field(description="Actionable suggestion for the Skills section")
    Experience: str = Field(description="Actionable suggestion for the Experience section")
    Projects: str = Field(description="Actionable suggestion for the Projects section")

class ResumeAnalysisOutput(BaseModel):
    ats_score: int = Field(description="ATS Score (0-100)")
    matched_skills: list[str] = Field(description="List of matched skills found in the resume")
    missing_keywords: list[str] = Field(description="List of missing keywords that should be added")
    resume_improvements: list[str] = Field(description="List of actionable resume improvements")
    section_wise_suggestions: SectionSuggestions = Field(description="Section-by-section specific suggestions")
    final_verdict: str = Field(description="A 2-3 line final evaluation of the resume")

# ─── SINGLE PRODUCTION-READY PROMPT ──────────────────────────────────────────

LLM_PROMPT = """You are an advanced ATS (Applicant Tracking System) Resume Analyzer.

Your job is to simulate how real ATS systems evaluate resumes before a recruiter sees them.

You must analyze the given resume against the provided job role and return exactly the requested JSON schema.

Follow these steps internally while analyzing:

Step 1: Understand Inputs
- Resume text
- Job role / job description

Step 2: Extract important information from resume:
- Skills
- Tools
- Technologies
- Experience
- Projects
- Education
- Achievements

Step 3: Extract job role requirements:
- Required skills
- Preferred skills
- Tools
- Experience
- Responsibilities
- Keywords

Step 4: Compare Resume vs Job Role
Identify:
- Matching skills
- Missing keywords
- Weak sections
- Irrelevant content

Step 5: Calculate ATS Score based on:
- Skill match (40%)
- Experience match (20%)
- Project relevance (15%)
- Keyword density (15%)
- Resume quality & structure (10%)

Step 6: Generate improvements
Suggest:
- Missing skills to add
- Better bullet points
- Stronger summary
- Better project descriptions
- Quantified achievements

Resume:
{resume}

Job Role:
{job_role}

You MUST return the output STRICTLY in the following JSON format. Do not include any tags like <think> or markdown code blocks around the JSON.
{format_instructions}
"""

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
=======
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
>>>>>>> 95a4aa9 (Till the alumni, student and admin)


def analyze_resume_with_ai(resume_text: str, target_role: str = '') -> dict:
    """
<<<<<<< HEAD
    Main entry point. Passes the resume and target role to the LLM using the 
    single production-ready prompt and parses the structured JSON output.
    """
    target_role = target_role.strip() or "General Role"
    
    # Initialize LLM and Parser
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    try:
        llm = HuggingFaceEndpoint(
            repo_id="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
            task="text-generation",
            temperature=0.4,
            max_new_tokens=1500,
            huggingfacehub_api_token=token,
        )
        model = ChatHuggingFace(llm=llm)
        parser = JsonOutputParser(pydantic_object=ResumeAnalysisOutput)
        
        prompt = LLM_PROMPT.format(
            resume=resume_text[:3000].replace('{', '{{').replace('}', '}}'),
            job_role=target_role.replace('{', '{{').replace('}', '}}'),
            format_instructions=parser.get_format_instructions().replace('{', '{{').replace('}', '}}')
        )

        response = model.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()

        # Remove <think> tags from DeepSeek output before parsing
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        
        # Sometime LLMs wrap json in markdown blocks, let's strip it
        if content.startswith('```json'):
            content = content.replace('```json', '', 1)
        if content.startswith('```'):
            content = content.replace('```', '', 1)
        if content.endswith('```'):
            content = content[::-1].replace('```', '', 1)[::-1]
        content = content.strip()

        # Parse JSON output to Pydantic object
        parsed_result = parser.parse(content)
        
        # Map the clean parsed JSON back to the legacy dictionary format expected by result.html
        return {
            "ats_score": parsed_result.get("ats_score", 0),
            "overall_summary": parsed_result.get("final_verdict", "Analysis complete."),
            "section_feedback": {
                "contact_information": {"score": 100, "feedback": "", "missing": []}, # Not covered by new prompt
                "education":           {"score": 100, "feedback": "", "missing": []}, # Not covered by new prompt
                "experience":          {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Experience", ""), "missing": []},
                "skills":              {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Skills", ""), "missing": []},
                "projects":            {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Projects", ""), "missing": []},
                "summary":             {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Summary", ""), "missing": []},
            },
            "keywords_present":  parsed_result.get("matched_skills", []),
            "keywords_missing":  parsed_result.get("missing_keywords", []),
            "improvements":      parsed_result.get("resume_improvements", []),
            "suggestions":       [], # We are mapping improvements directly, leave suggestions empty to avoid redundancy
            "strengths":         [], # Not requested in new prompt
            "formatting_tips":   [], # Not requested in new prompt
        }

    except Exception as e:
        print(f"[LLM Error] {e}")
        # Graceful fallback if LLM parsing fails completely
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
=======
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
>>>>>>> 95a4aa9 (Till the alumni, student and admin)

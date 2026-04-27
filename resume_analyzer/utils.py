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


def analyze_resume_with_ai(resume_text: str, target_role: str = '') -> dict:
    """
    Main entry point. Passes the resume and target role to the LLM using the
    single production-ready prompt and parses the structured JSON output.
    """
    target_role = target_role.strip() or "General Role"

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

        # Strip markdown code blocks if LLM wraps the JSON
        if content.startswith('```json'):
            content = content.replace('```json', '', 1)
        if content.startswith('```'):
            content = content.replace('```', '', 1)
        if content.endswith('```'):
            content = content[::-1].replace('```', '', 1)[::-1]
        content = content.strip()

        # Parse JSON output to Pydantic object
        parsed_result = parser.parse(content)

        # Map the parsed JSON back to the legacy dictionary format expected by result.html
        return {
            "ats_score": parsed_result.get("ats_score", 0),
            "overall_summary": parsed_result.get("final_verdict", "Analysis complete."),
            "section_feedback": {
                "contact_information": {"score": 100, "feedback": "", "missing": []},
                "education":           {"score": 100, "feedback": "", "missing": []},
                "experience":          {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Experience", ""), "missing": []},
                "skills":              {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Skills", ""), "missing": []},
                "projects":            {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Projects", ""), "missing": []},
                "summary":             {"score": parsed_result.get("ats_score", 0), "feedback": parsed_result.get("section_wise_suggestions", {}).get("Summary", ""), "missing": []},
            },
            "keywords_present":  parsed_result.get("matched_skills", []),
            "keywords_missing":  parsed_result.get("missing_keywords", []),
            "improvements":      parsed_result.get("resume_improvements", []),
            "suggestions":       [],
            "strengths":         [],
            "formatting_tips":   [],
        }

    except Exception as e:
        print(f"[LLM Error] {e}")
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

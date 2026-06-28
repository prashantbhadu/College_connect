import sys
sys.path.insert(0, '.')

# Set up Django environment
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')
django.setup()

# Now test the analyzer
from resume_analyzer.utils import analyze_resume_with_ai

sample_resume = """
John Doe
Backend Python Developer
Email: john@example.com | Phone: +91-9999999999

SKILLS:
Python, Django, REST APIs, PostgreSQL, Redis, Docker, Git, Linux

EXPERIENCE:
Backend Developer at TechCorp (2022 - Present)
- Built RESTful APIs using Django REST Framework serving 100k+ users
- Optimized PostgreSQL queries reducing response time by 40%
- Deployed services using Docker and AWS EC2

PROJECTS:
CampusConnect (Django, PostgreSQL, Bootstrap)
- Student networking platform with resume analyzer feature
- Integrated AI using Hugging Face APIs

EDUCATION:
B.Tech Computer Science, 2022
"""

print("Testing full AI analysis pipeline...")
result = analyze_resume_with_ai(sample_resume, "Backend Python Developer")
print(f"ATS Score: {result['ats_score']}")
print(f"Overall Summary: {result['overall_summary'][:150]}...")
print(f"Keywords Present ({len(result['keywords_present'])}): {result['keywords_present'][:5]}")
print(f"Keywords Missing ({len(result['keywords_missing'])}): {result['keywords_missing'][:5]}")
print(f"Improvements ({len(result['improvements'])}): {result['improvements'][:2]}")
print("\n✅ SUCCESS - Resume analyzer is working!")

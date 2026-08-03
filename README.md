# 🎓 CampusConnect — AI-Powered Campus Placement & Networking Platform

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.9-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Structured_Output-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![DeepSeek](https://img.shields.io/badge/DeepSeek_R1-AI_Engine-FF6B6B?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Email](https://img.shields.io/badge/Email-Notifications-D44638?style=for-the-badge&logo=gmail&logoColor=white)

**A full-stack Django web application that connects students, alumni, and campus placement opportunities — powered by an AI Resume Analyzer using DeepSeek-R1 and LangChain Structured Outputs.**

[Features](#-features) · [Tech Stack](#-tech-stack) · [Installation](#-installation) · [Usage](#-usage) · [Project Structure](#-project-structure)

</div>

---

## 📖 About

**CampusConnect** is a production-grade campus networking platform designed to solve three critical problems faced by college students:

1. **Missing placement deadlines** due to scattered information
2. **No direct access** to alumni working in the industry
3. **Weak resumes** that fail to pass Applicant Tracking Systems (ATS)

The platform brings everything under one roof — a unified dashboard for placement drives, an alumni mentorship network, and an **AI-powered resume analyzer** that uses the DeepSeek-R1 LLM to provide instant, structured ATS feedback.

---

## ✨ Features

### 🤖 AI Resume Analyzer (LangChain + DeepSeek-R1)
- **Instant ATS Scoring** — Upload your resume (PDF/DOCX) and get a score out of 100 based on how well it matches a target job role
- **Structured JSON Output** — Uses LangChain's `JsonOutputParser` with Pydantic schemas to guarantee reliable, parseable AI responses
- **Missing Keywords Detection** — The AI identifies critical skills and keywords absent from your resume
- **Section-wise Feedback** — Get targeted improvement suggestions for Summary, Skills, Experience, and Projects sections
- **Final Verdict** — A concise 2-3 line evaluation summarizing your resume's strengths and gaps
- **Resume History** — All past analyses are stored in the database for comparison over time

### 💼 Campus Placement Tracking
- **Live Placement Feed** — View all active campus drives with company details, roles, CTC, and deadlines
- **CGPA-Based Eligibility** — Automatically filters opportunities based on your academic performance
- **Application Tracking** — Apply to drives and track your application status from a single dashboard
- **Placement Calendar** — Visual calendar view of upcoming campus drive deadlines
- **Admin Posting** — Admins and alumni can post new placement opportunities with company logos

### 📧 Email Notification System
- **Automatic Alerts** — Every registered student receives an email the moment a new placement or internship post goes live
- **Zero Delay** — Notifications fire instantly via a Django `post_save` signal attached to `PlacementPost`
- **Async Delivery** — Emails are dispatched in a background daemon thread using Python's `threading` module, so the web request is never blocked
- **Bulk Sending** — Uses Django's `send_mass_mail` to open a single SMTP connection and deliver all emails efficiently in one batch
- **Smart Targeting** — Only students with a registered email address receive notifications; no spam to users with missing emails
- **Key Details Included** — Each email contains the company name, role title, and application deadline so students have everything at a glance
- **Gmail SMTP Ready** — Pre-configured for Gmail SMTP with TLS; swap to any SMTP provider via `.env` variables
- **Console Backend for Dev** — Emails print to the terminal in development (`EMAIL_BACKEND=console`) and switch to real SMTP in production

### 🤝 Alumni Network & Mentorship
- **Alumni Directory** — Browse verified alumni profiles with their current company, role, and expertise
- **Industry Insights** — Alumni share posts categorized by type (Career Tips, Interview Prep, Industry Trends)
- **1:1 Mentorship** — Students can request direct mentorship from alumni professionals
- **Post Categories** — Organized insight feed with tags and search functionality

### 👤 User Management
- **Dual Registration** — Separate signup flows for Students and Alumni with role-specific fields
- **Rich Profiles** — Profile pictures, bio, skills, GitHub/LinkedIn URLs, portfolio links
- **CGPA Tracking** — Semester-wise GPA entry with automatic CGPA calculation
- **Profile Completion** — Visual indicators prompting users to complete their profiles

### 📊 Dashboard
- **Unified Feed** — See latest placements, alumni posts, and upcoming deadlines in one view
- **Smart Sidebar** — Profile card, upcoming deadline alerts, and quick action shortcuts
- **Global Search** — Search across placements, alumni posts, and people simultaneously

### 🎨 Modern Landing Page
- **Stunning Hero Section** — Real campus imagery with gradient overlays and parallax scrolling
- **Feature Showcase** — Interactive feature cards highlighting the AI Analyzer, Placements, and Alumni modules
- **Responsive Design** — Fully mobile-responsive with Bootstrap 5 dark theme

---

## 🏗 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2.9, Django REST Framework |
| **Frontend** | Bootstrap 5.3, Bootstrap Icons, Google Fonts (Inter) |
| **AI Engine** | DeepSeek-R1-Distill-Llama-8B via Hugging Face API |
| **LLM Framework** | LangChain (`ChatHuggingFace`, `JsonOutputParser`, Pydantic) |
| **Database** | SQLite (dev) / PostgreSQL (prod-ready) |
| **Auth** | Django built-in + JWT (SimpleJWT) for API |
| **File Parsing** | PyPDF2 (PDF), python-docx (DOCX) |
| **Static Files** | WhiteNoise |
| **Styling** | Custom CSS with dark mode, glassmorphism, micro-animations |
| **Email** | Django `send_mass_mail`, Gmail SMTP / any SMTP, async via `threading` |

---

## 🔑 What Makes This Project Unique

### 1. Production-Grade LLM Pipeline
Unlike simple OpenAI API wrappers, CampusConnect uses a **structured output architecture**:
- A comprehensive 6-step analysis prompt guides the LLM through resume evaluation
- **Pydantic schemas** enforce the exact JSON structure the frontend expects
- `<think>` tag stripping and markdown cleanup ensure robust parsing from the DeepSeek model
- Graceful error fallback if the LLM fails

### 2. Real ATS Simulation
The AI doesn't just count keywords — it simulates actual ATS scoring:
- **Skill Match** (40%) — Direct comparison against role requirements
- **Experience Match** (20%) — Relevance and depth of work history
- **Project Relevance** (15%) — Quality and alignment of projects
- **Keyword Density** (15%) — Presence of industry-standard terminology
- **Resume Structure** (10%) — Formatting, sections, and readability

### 3. Role-Based Access Control
Three user types (Student, Alumni, Admin) with different permissions:
- Students can apply to placements and request mentorship
- Alumni can post opportunities, share insights, and mentor students
- Admins have full Django admin panel access

### 4. CGPA-Aware System
- Students enter semester-wise GPAs; the system auto-computes CGPA
- Placement opportunities have minimum CGPA thresholds
- Ineligible drives are automatically filtered from the student's view

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/prashantbhadu/College_connect.git
cd College_connect

# 2. Create and activate virtual environment
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install AI dependencies (for Resume Analyzer)
pip install langchain-huggingface langchain-core python-dotenv

# 5. Create .env file
cp .env.example .env
# Edit .env with your credentials:
#   HUGGINGFACEHUB_API_TOKEN=hf_your_token_here   ← required for AI Resume Analyzer
#   EMAIL_HOST_USER=your@gmail.com                 ← required for email notifications
#   EMAIL_HOST_PASSWORD=your-gmail-app-password    ← use a Gmail App Password, not your real password
#
# For local development, keep EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# Emails will print in the terminal instead of being sent.
# Switch to django.core.mail.backends.smtp.EmailBackend for real sending.

# 6. Run migrations
python manage.py migrate

# 7. Create a superuser
python manage.py createsuperuser

# 8. Start the development server
python manage.py runserver
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key |
| `DEBUG` | ✅ | Set to `True` for development |
| `HUGGINGFACEHUB_API_TOKEN` | ✅ | Hugging Face API token (AI Resume Analyzer) |
| `EMAIL_BACKEND` | ✅ | `console` for dev, `smtp.EmailBackend` for prod |
| `EMAIL_HOST` | ✅ | SMTP server — default `smtp.gmail.com` |
| `EMAIL_PORT` | ✅ | SMTP port — default `587` (TLS) |
| `EMAIL_USE_TLS` | ✅ | Set `True` for TLS encryption |
| `EMAIL_HOST_USER` | ✅ | Your sender Gmail address |
| `EMAIL_HOST_PASSWORD` | ✅ | Gmail App Password (not your account password) |

---

## 🚀 Usage

1. **Visit** `http://127.0.0.1:8000/` — You'll see the landing page
2. **Register** as a Student or Alumni
3. **Complete your profile** — Add skills, CGPA, links
4. **Browse Placements** — View drives and apply to eligible ones
5. **Analyze Your Resume** — Upload a PDF/DOCX and select a target role
6. **Connect with Alumni** — Browse the directory and request mentorship
7. **Admin Panel** — Visit `/admin/` to manage data

### 📬 How Email Notifications Work

Whenever an admin or alumni posts a new placement or internship opportunity:

1. Django fires a `post_save` signal on the `PlacementPost` model
2. `notify_students_new_placement` in `placements/signals.py` catches the signal (only for newly **created** and **active** posts)
3. `send_placement_emails_async` in `placements/utils.py` spins up a **background daemon thread**
4. Inside the thread, all student accounts with a registered email are fetched
5. A single SMTP connection is opened and all emails are sent in one batch via `send_mass_mail`
6. The student receives an email with the **company name**, **role**, and **application deadline**

> **Gmail App Password**: Go to your Google Account → Security → 2-Step Verification → App Passwords, generate one, and paste it into `EMAIL_HOST_PASSWORD` in your `.env`.

---

## 📁 Project Structure

```
collegeconnect/
├── accounts/              # User authentication, profiles, CGPA
│   ├── models.py          # UserProfile (AbstractUser), SemesterGPA
│   ├── views.py           # Login, register, profile views
│   └── forms.py           # Registration and profile forms
│
├── alumni/                # Alumni network & mentorship
│   ├── models.py          # AlumniPost, MentorshipRequest
│   ├── views.py           # Directory, posts, mentorship
│   └── templates/         # Alumni-specific templates
│
├── placements/            # Campus placement management
│   ├── models.py          # PlacementPost, Application, PlacementRecord
│   ├── views.py           # List, detail, apply, calendar
│   ├── signals.py         # post_save signal → triggers email on new post
│   ├── utils.py           # send_placement_emails_async (background thread + send_mass_mail)
│   └── templates/         # Placement-specific templates
│
├── resume_analyzer/       # AI-powered resume analysis
│   ├── utils.py           # LangChain pipeline, Pydantic schemas, LLM prompt
│   ├── models.py          # ResumeAnalysis (stores results)
│   ├── views.py           # Upload, result, history views
│   └── templates/         # Upload form and result dashboard
│
├── dashboard/             # Landing page & main feed
│   ├── views.py           # Landing page, feed, search
│   └── urls.py            # Route "/" to landing, "/dashboard/" to feed
│
├── templates/             # Global templates
│   ├── base.html          # Master layout (navbar, footer, dark theme)
│   └── dashboard/         # Landing page, feed, search results
│
├── static/
│   ├── css/custom.css     # Custom dark-mode CSS, animations
│   ├── js/main.js         # Frontend JavaScript
│   └── images/            # Landing page campus images
│
├── campusconnect/         # Django project settings
│   ├── settings.py
│   └── urls.py
│
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── manage.py
```

---

## 📸 Screenshots

> Upload screenshots of your landing page, dashboard, and resume analyzer results to the `static/images/` directory and reference them here.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is built for educational purposes as part of a college project.

---

## 👨‍💻 Author

**Prashant Bhadu**
- GitHub: [@prashantbhadu](https://github.com/prashantbhadu)

---

<div align="center">
  <sub>Built with ❤️ for students, by students.</sub>
</div>

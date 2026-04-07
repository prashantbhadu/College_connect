# College_connect
# CampusConnect

A modern student networking and placement management platform built with Django, Bootstrap 5, and OpenAI.

## Features

- **Role-based Access**: Separate dashboards and profiles for Students and Alumni.
- **AI Resume Analyzer**: Upload your resume (PDF/DOCX) and get an instant ATS score, missing keywords, and improvement tips powered by OpenAI.
- **Placements & Internships**: Browse opportunities, apply directly, and participate in company-specific discussion threads.
- **Alumni Network**: Connect with alumni, request mentorship, ask questions, and read their success stories and guidance posts.
- **Dark Theme UI**: Premium, responsive user interface with dynamic animations and gradients.

## Quick Start (Local Setup)

### Prerequisites

- Python 3.9+
- PostgreSQL (or use the default SQLite config for testing)
- OpenAI API Key (optional, falls back to mock analysis if not provided)

### 1. Clone & Setup Environment

```powershell
# Create virtual environment
python -m venv env

# Activate environment (Windows)
.\env\Scripts\activate
# OR on Mac/Linux: source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

1. Copy `.env.example` to `.env`:
   ```powershell
   cp .env.example .env
   ```
2. Update the `.env` file with your details.
   - If `USE_POSTGRES=False`, the app will use SQLite.
   - Add your `OPENAI_API_KEY` to enable real AI resume analysis.

### 3. Database & Demo Data

Run the following commands to initialize the database and populate it with sample data:

```powershell
# Apply database migrations
python manage.py migrate

# Load demo users, placements, and alumni posts
python create_demo_data.py
```

### 4. Run Server

```powershell
# Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Demo Credentials

If you ran `create_demo_data.py`, you can log in with:

| Role | Username | Password |
|------|----------|----------|
| **Student** | `student1` | `Test@1234` |
| **Alumni** | `alumni1` | `Test@1234` |
| **Admin** | `admin` | `admin@123` |

## App Structure
- `accounts`: User authentication, custom profiles, and skills.
- `placements`: Job postings, applications, and threads.
- `alumni`: Directory, insights, mentorship requests, and queries.
- `resume_analyzer`: AI-powered ATS scoring and feedback.
- `dashboard`: Centralized feed and cross-model search.

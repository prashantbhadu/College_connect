from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResumeAnalysis
from .forms import ResumeUploadForm
from .utils import extract_text_from_file, analyze_resume_with_ai


@login_required
def resume_upload(request):
    form = ResumeUploadForm()
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume_file']
            target_role = form.cleaned_data.get('target_role', '')

            # Extract text
            resume_text = extract_text_from_file(uploaded_file)
            uploaded_file.seek(0)  # Reset after reading

            # AI analysis
            messages.info(request, 'Analyzing your resume...')
            analysis_data = analyze_resume_with_ai(resume_text, target_role)

            # Save to DB
            analysis = ResumeAnalysis.objects.create(
                user=request.user,
                resume_file=uploaded_file,
                target_role=target_role,
                ats_score=analysis_data.get('ats_score', 0),
                analysis_result=analysis_data,
                suggestions=analysis_data.get('suggestions', []),
            )

            messages.success(request, 'Resume analyzed successfully!')
            return redirect('resume_analyzer:result', pk=analysis.pk)

    history = ResumeAnalysis.objects.filter(user=request.user)[:5]
    return render(request, 'resume_analyzer/upload.html', {'form': form, 'history': history})


@login_required
def resume_result(request, pk):
    analysis = get_object_or_404(ResumeAnalysis, pk=pk, user=request.user)
    data = analysis.analysis_result

    section_feedback = data.get('section_feedback', {})
    sections = [
        {'name': 'Contact Information', 'key': 'contact_information', 'icon': 'bi-person-badge'},
        {'name': 'Education', 'key': 'education', 'icon': 'bi-mortarboard'},
        {'name': 'Experience', 'key': 'experience', 'icon': 'bi-briefcase'},
        {'name': 'Skills', 'key': 'skills', 'icon': 'bi-tools'},
        {'name': 'Projects', 'key': 'projects', 'icon': 'bi-code-slash'},
    ]

    for s in sections:
        s['data'] = section_feedback.get(s['key'], {})

    context = {
        'analysis': analysis,
        'data': data,
        'sections': sections,
        'ats_score': analysis.ats_score,
        'ats_color': _score_color(analysis.ats_score),
        'ats_label': _score_label(analysis.ats_score),
    }
    return render(request, 'resume_analyzer/result.html', context)


@login_required
def resume_history(request):
    analyses = ResumeAnalysis.objects.filter(user=request.user)
    return render(request, 'resume_analyzer/history.html', {'analyses': analyses})


def _score_color(score):
    if score >= 80:
        return '#22c55e'  # green
    elif score >= 60:
        return '#f59e0b'  # amber
    elif score >= 40:
        return '#f97316'  # orange
    return '#ef4444'   # red


def _score_label(score):
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Needs Work'
    return 'Poor'

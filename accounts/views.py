from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile, Skill
from .forms import StudentRegistrationForm, AlumniRegistrationForm, ProfileUpdateForm


def home(request):
    return redirect('dashboard:feed')


def register_student(request):
    if request.user.is_authenticated:
        return redirect('dashboard:feed')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Complete your profile to get started.')
            return redirect('accounts:profile_edit')
        else:
            messages.error(request, 'Registration failed. Please check the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form})


def register_alumni(request):
    if request.user.is_authenticated:
        return redirect('dashboard:feed')
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Complete your profile.')
            return redirect('accounts:profile_edit')
        else:
            messages.error(request, 'Registration failed. Please check the errors below.')
    else:
        form = AlumniRegistrationForm()
    return render(request, 'accounts/register_alumni.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:feed')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'dashboard:feed')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request, pk=None):
    if pk:
        user = get_object_or_404(UserProfile, pk=pk)
    else:
        user = request.user
    return render(request, 'accounts/profile.html', {'profile_user': user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile', pk=request.user.pk)
    else:
        # Pre-fill skills input
        current_skills = ', '.join(request.user.skills.values_list('name', flat=True))
        form = ProfileUpdateForm(instance=request.user, initial={'skills_input': current_skills})
    return render(request, 'accounts/profile_edit.html', {'form': form})

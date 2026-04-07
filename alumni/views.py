from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from accounts.models import UserProfile
from .models import AlumniPost, MentorshipRequest, AlumniQuery
from .forms import AlumniPostForm, MentorshipRequestForm, AlumniQueryForm, QueryAnswerForm


def alumni_directory(request):
    alumni = UserProfile.objects.filter(user_type='alumni')

    # Filters
    batch = request.GET.get('batch')
    company = request.GET.get('company')
    branch = request.GET.get('branch')
    search = request.GET.get('q')

    if batch:
        alumni = alumni.filter(graduation_year=batch)
    if company:
        alumni = alumni.filter(current_company__icontains=company)
    if branch:
        alumni = alumni.filter(branch=branch)
    if search:
        alumni = alumni.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(current_company__icontains=search) |
            Q(current_role__icontains=search)
        )

    batches = UserProfile.objects.filter(
        user_type='alumni', graduation_year__isnull=False
    ).values_list('graduation_year', flat=True).distinct().order_by('-graduation_year')

    context = {
        'alumni': alumni,
        'batches': batches,
        'branch_choices': UserProfile.BRANCH_CHOICES,
        'selected_batch': batch,
        'selected_company': company,
        'selected_branch': branch,
    }
    return render(request, 'alumni/directory.html', context)


def alumni_post_list(request):
    posts = AlumniPost.objects.select_related('author').all()
    post_type = request.GET.get('type')
    if post_type:
        posts = posts.filter(post_type=post_type)
    return render(request, 'alumni/post_list.html', {'posts': posts, 'POST_TYPE_CHOICES': AlumniPost.POST_TYPE_CHOICES})


def alumni_post_detail(request, pk):
    post = get_object_or_404(AlumniPost, pk=pk)
    return render(request, 'alumni/post_detail.html', {'post': post})


@login_required
def alumni_post_create(request):
    if not request.user.is_alumni:
        messages.error(request, 'Only alumni can create posts.')
        return redirect('alumni:post_list')
    if request.method == 'POST':
        form = AlumniPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post published!')
            return redirect('alumni:post_detail', pk=post.pk)
    else:
        form = AlumniPostForm()
    return render(request, 'alumni/post_create.html', {'form': form})


@login_required
def like_post(request, pk):
    post = get_object_or_404(AlumniPost, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('alumni:post_detail', pk=pk)


@login_required
def mentorship_request(request, alumni_pk):
    alumni = get_object_or_404(UserProfile, pk=alumni_pk, user_type='alumni')
    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.from_user = request.user
            req.to_alumni = alumni
            req.save()
            messages.success(request, f'Mentorship request sent to {alumni.get_full_name()}!')
            return redirect('alumni:directory')
    else:
        form = MentorshipRequestForm()
    return render(request, 'alumni/mentorship.html', {'form': form, 'alumni': alumni})


@login_required
def my_mentorship_requests(request):
    if request.user.is_alumni:
        requests_received = MentorshipRequest.objects.filter(to_alumni=request.user)
        return render(request, 'alumni/mentorship_manage.html', {'requests': requests_received})
    else:
        requests_sent = MentorshipRequest.objects.filter(from_user=request.user)
        return render(request, 'alumni/mentorship_sent.html', {'requests': requests_sent})


@login_required
def respond_mentorship(request, pk):
    req = get_object_or_404(MentorshipRequest, pk=pk, to_alumni=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['accepted', 'declined']:
            req.status = action
            req.response_message = request.POST.get('response_message', '')
            req.save()
            messages.success(request, f'Request {action}.')
    return redirect('alumni:my_mentorship')


@login_required
def ask_query(request, alumni_pk):
    alumni = get_object_or_404(UserProfile, pk=alumni_pk, user_type='alumni')
    if request.method == 'POST':
        form = AlumniQueryForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.from_user = request.user
            q.to_alumni = alumni
            q.save()
            messages.success(request, 'Your question was sent!')
            return redirect('alumni:directory')
    else:
        form = AlumniQueryForm()
    return render(request, 'alumni/query_ask.html', {'form': form, 'alumni': alumni})


@login_required
def my_queries(request):
    if request.user.is_alumni:
        queries = AlumniQuery.objects.filter(to_alumni=request.user)
    else:
        queries = AlumniQuery.objects.filter(from_user=request.user)
    return render(request, 'alumni/queries.html', {'queries': queries})


@login_required
def answer_query(request, pk):
    query = get_object_or_404(AlumniQuery, pk=pk, to_alumni=request.user)
    if request.method == 'POST':
        form = QueryAnswerForm(request.POST, instance=query)
        if form.is_valid():
            q = form.save(commit=False)
            q.is_answered = True
            q.answered_at = timezone.now()
            q.save()
            messages.success(request, 'Answer saved!')
    return redirect('alumni:my_queries')

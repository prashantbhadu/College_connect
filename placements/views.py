from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import PlacementPost, Application, CompanyThread
from .forms import PlacementPostForm, ThreadMessageForm


def placement_list(request):
    posts = PlacementPost.objects.filter(is_active=True)

    # Filters
    role_type = request.GET.get('role_type')
    company = request.GET.get('company')
    search = request.GET.get('q')

    if role_type:
        posts = posts.filter(role_type=role_type)
    if company:
        posts = posts.filter(company_name__icontains=company)
    if search:
        posts = posts.filter(
            Q(company_name__icontains=search) |
            Q(role__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Eligibility Filtering for Students
    is_cgpa_missing = False
    if request.user.is_authenticated and request.user.is_student:
        if request.user.cgpa is not None:
            posts = posts.filter(min_cgpa__lte=request.user.cgpa)
        else:
            is_cgpa_missing = True
            posts = posts.none()  # Only show eligible ones, so none if missing

    # Annotate applied status for logged-in users
    applied_ids = set()
    if request.user.is_authenticated:
        applied_ids = set(Application.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True))

    context = {
        'posts': posts,
        'applied_ids': applied_ids,
        'today': timezone.now().date(),
        'role_type': role_type,
        'search': search,
        'is_cgpa_missing': is_cgpa_missing,
    }
    return render(request, 'placements/list.html', context)


def placement_detail(request, pk):
    post = get_object_or_404(PlacementPost, pk=pk)
    threads = post.threads.select_related('author').all()
    applied = False
    if request.user.is_authenticated:
        applied = Application.objects.filter(post=post, user=request.user).exists()

    thread_form = ThreadMessageForm()
    if request.method == 'POST' and request.user.is_authenticated:
        thread_form = ThreadMessageForm(request.POST)
        if thread_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.post = post
            thread.author = request.user
            thread.save()
            messages.success(request, 'Message posted!')
            return redirect('placements:detail', pk=pk)

    applicants = []
    if request.user.is_authenticated and (request.user.is_staff or post.posted_by == request.user):
        applicants = post.applications.select_related('user').all()

    is_eligible = True
    if request.user.is_authenticated and request.user.is_student:
        if request.user.cgpa is None or request.user.cgpa < post.min_cgpa:
            is_eligible = False

    context = {
        'post': post,
        'threads': threads,
        'thread_form': thread_form,
        'applied': applied,
        'applicants': applicants,
        'is_eligible': is_eligible,
    }
    return render(request, 'placements/detail.html', context)


@login_required
def placement_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can post new opportunities.')
        return redirect('placements:list')
        
    if request.method == 'POST':
        form = PlacementPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.save()
            messages.success(request, 'Placement opportunity posted successfully!')
            return redirect('placements:detail', pk=post.pk)
        else:
            print(form.errors)
            messages.error(request, 'Failed to post opportunity. Please try again.')    
    else:
        form = PlacementPostForm()
    return render(request, 'placements/create.html', {'form': form})


@login_required
def placement_update(request, pk):
    post = get_object_or_404(PlacementPost, pk=pk)
    # Check if user is the poster or an admin
    if post.posted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this opportunity.')
        return redirect('placements:detail', pk=pk)
        
    if request.method == 'POST':
        form = PlacementPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Placement opportunity updated successfully!')
            return redirect('placements:detail', pk=pk)
    else:
        form = PlacementPostForm(instance=post)
    return render(request, 'placements/create.html', {'form': form, 'edit_mode': True})


@login_required
def placement_delete(request, pk):
    post = get_object_or_404(PlacementPost, pk=pk)
    if post.posted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this opportunity.')
        return redirect('placements:detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Placement opportunity deleted.')
        return redirect('placements:list')
    return render(request, 'placements/delete_confirm.html', {'post': post})


@login_required
def apply_placement(request, pk):
    post = get_object_or_404(PlacementPost, pk=pk)
    
    if request.user.is_student:
        if request.user.cgpa is None or request.user.cgpa < post.min_cgpa:
            messages.error(request, 'You do not meet the minimum CGPA requirement for this opportunity.')
            return redirect('placements:detail', pk=pk)

    if request.method == 'POST':
        obj, created = Application.objects.get_or_create(post=post, user=request.user)
        if created:
            messages.success(request, f'Successfully applied to {post.company_name}!')
        else:
            messages.info(request, 'You have already applied to this position.')
    return redirect('placements:detail', pk=pk)


@login_required
def my_applications(request):
    apps = Application.objects.filter(user=request.user).select_related('post')
    return render(request, 'placements/my_applications.html', {'applications': apps})


def placement_calendar(request):
    upcoming = PlacementPost.objects.filter(
        is_active=True,
        deadline__gte=timezone.now().date()
    ).order_by('deadline')
    return render(request, 'placements/calendar.html', {'upcoming': upcoming})

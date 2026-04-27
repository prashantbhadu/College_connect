import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg, Max
from django.utils import timezone
from .models import PlacementPost, Application, CompanyThread, PlacementRecord
from .forms import PlacementPostForm, ThreadMessageForm, PlacementRecordForm


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
    if request.user.is_authenticated and (request.user.is_admin or post.posted_by == request.user):
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
        'today': timezone.now().date(),
    }
    return render(request, 'placements/detail.html', context)


@login_required
def placement_create(request):
    if not request.user.is_admin:
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
    if post.posted_by != request.user and not request.user.is_admin:
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
    if post.posted_by != request.user and not request.user.is_admin:
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


def _require_admin(user):
    return user.is_authenticated and user.is_admin


@login_required
def placement_statistics(request):
    records = PlacementRecord.objects.select_related('student', 'placement_post', 'recorded_by')

    year = request.GET.get('year', '').strip()
    branch = request.GET.get('branch', '').strip()
    company = request.GET.get('company', '').strip()
    status = request.GET.get('status', '').strip()
    search = request.GET.get('q', '').strip()

    if year:
        records = records.filter(placement_year=year)
    if branch:
        records = records.filter(branch=branch)
    if company:
        records = records.filter(company_name__icontains=company)
    if status:
        records = records.filter(placement_status=status)
    if search:
        records = records.filter(
            Q(student__username__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(company_name__icontains=search) |
            Q(role__icontains=search)
        )

    stats = records.aggregate(
        total_records=Count('id'),
        total_students=Count('student', distinct=True),
        total_companies=Count('company_name', distinct=True),
        avg_package=Avg('package_lpa'),
        highest_package=Max('package_lpa'),
    )

    year_options = PlacementRecord.objects.order_by('-placement_year').values_list('placement_year', flat=True).distinct()
    branch_options = list(
        PlacementRecord.objects.order_by('branch').exclude(branch='').values_list('branch', flat=True).distinct()
    )
    status_options = PlacementRecord.PLACEMENT_STATUS_CHOICES

    company_chart = list(
        records.values('company_name').annotate(total=Count('id')).order_by('-total', 'company_name')[:7]
    )
    branch_chart_raw = list(
        records.values('branch').exclude(branch='').annotate(total=Count('id')).order_by('-total', 'branch')
    )
    yearly_chart = list(
        records.values('placement_year').annotate(total=Count('id')).order_by('placement_year')
    )
    branch_label_map = dict(PlacementRecord._meta.get_field('branch').choices)
    branch_chart = [
        {'branch': branch_label_map.get(item['branch'], item['branch']), 'total': item['total']}
        for item in branch_chart_raw
    ]

    context = {
        'records': records[:50],
        'stats': stats,
        'year_options': year_options,
        'branch_options': branch_options,
        'status_options': status_options,
        'selected_year': year,
        'selected_branch': branch,
        'selected_company': company,
        'selected_status': status,
        'search': search,
        'company_chart_json': json.dumps(company_chart),
        'branch_chart_json': json.dumps(branch_chart),
        'yearly_chart_json': json.dumps(yearly_chart),
        'branch_filter_choices': [
            (value, label) for value, label in PlacementRecord._meta.get_field('branch').choices
            if value in branch_options
        ],
        'record_count': records.count(),
        'can_manage_statistics': request.user.is_admin,
    }
    return render(request, 'placements/statistics.html', context)


@login_required
def placement_record_create(request):
    if not _require_admin(request.user):
        messages.error(request, 'Only admins can add placement records.')
        return redirect('placements:list')

    if request.method == 'POST':
        form = PlacementRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.recorded_by = request.user
            record.save()
            messages.success(request, 'Placement record added successfully.')
            return redirect('placements:statistics')
    else:
        initial = {
            'placement_year': timezone.now().year,
            'company_name': request.GET.get('company_name', '').strip(),
            'role': request.GET.get('role', '').strip(),
        }
        form = PlacementRecordForm(initial=initial)

    return render(request, 'placements/record_form.html', {'form': form, 'record_mode': 'create'})


@login_required
def placement_record_update(request, pk):
    if not _require_admin(request.user):
        messages.error(request, 'Only admins can update placement records.')
        return redirect('placements:list')

    record = get_object_or_404(PlacementRecord, pk=pk)
    if request.method == 'POST':
        form = PlacementRecordForm(request.POST, instance=record)
        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.recorded_by = request.user
            updated_record.save()
            messages.success(request, 'Placement record updated successfully.')
            return redirect('placements:statistics')
    else:
        form = PlacementRecordForm(instance=record)

    return render(
        request,
        'placements/record_form.html',
        {'form': form, 'record': record, 'record_mode': 'edit'}
    )


@login_required
def placement_record_delete(request, pk):
    if not _require_admin(request.user):
        messages.error(request, 'Only admins can delete placement records.')
        return redirect('placements:list')

    record = get_object_or_404(PlacementRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Placement record deleted successfully.')
        return redirect('placements:statistics')

    return render(request, 'placements/record_delete_confirm.html', {'record': record})

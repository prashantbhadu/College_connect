from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from placements.models import PlacementPost
from alumni.models import AlumniPost


def feed(request):
    recent_placements = PlacementPost.objects.filter(
        is_active=True
    ).select_related('posted_by')[:6]

    recent_alumni_posts = AlumniPost.objects.select_related('author')[:4]

    upcoming = PlacementPost.objects.filter(
        is_active=True,
        deadline__gte=timezone.now().date()
    ).order_by('deadline')[:5]

    context = {
        'recent_placements': recent_placements,
        'recent_alumni_posts': recent_alumni_posts,
        'upcoming': upcoming,
        'today': timezone.now().date(),
    }
    return render(request, 'dashboard/feed.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    results = {'placements': [], 'alumni_posts': [], 'people': []}

    if query:
        from accounts.models import UserProfile
        results['placements'] = PlacementPost.objects.filter(
            Q(company_name__icontains=query) |
            Q(role__icontains=query) |
            Q(description__icontains=query)
        )[:10]

        results['alumni_posts'] = AlumniPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )[:10]

        results['people'] = UserProfile.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(current_company__icontains=query) |
            Q(username__icontains=query)
        )[:10]

    return render(request, 'dashboard/search_results.html', {'query': query, 'results': results})

from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from placements.models import PlacementPost
from alumni.models import AlumniPost
from django.utils import timezone


class FeedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        placements = list(PlacementPost.objects.filter(is_active=True).values(
            'id', 'company_name', 'role', 'ctc', 'deadline', 'role_type'
        )[:10])
        alumni_posts = list(AlumniPost.objects.values(
            'id', 'title', 'post_type', 'created_at', 'author_id'
        )[:10])
        return Response({
            'placements': placements,
            'alumni_posts': alumni_posts,
        })


urlpatterns = [
    path('dashboard/feed/', FeedAPIView.as_view(), name='api_feed'),
]

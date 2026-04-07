from django.urls import path
from rest_framework import serializers, generics, permissions
from .models import AlumniPost
from accounts.models import UserProfile


class AlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'branch',
                  'graduation_year', 'current_company', 'current_role', 'bio', 'linkedin_url']


class AlumniPostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = AlumniPost
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username


class AlumniDirectoryAPIView(generics.ListAPIView):
    serializer_class = AlumniSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.filter(user_type='alumni')


class AlumniPostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AlumniPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = AlumniPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


urlpatterns = [
    path('alumni/', AlumniDirectoryAPIView.as_view(), name='api_alumni_directory'),
    path('alumni/posts/', AlumniPostListCreateAPIView.as_view(), name='api_alumni_posts'),
]

from django.urls import path
from rest_framework import serializers, generics, permissions
from .models import PlacementPost, Application


class PlacementSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PlacementPost
        fields = '__all__'
        read_only_fields = ['posted_by', 'created_at', 'updated_at']

    def get_posted_by_name(self, obj):
        return obj.posted_by.get_full_name() or obj.posted_by.username


class PlacementListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PlacementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = PlacementPost.objects.filter(is_active=True)
        role_type = self.request.query_params.get('role_type')
        if role_type:
            qs = qs.filter(role_type=role_type)
        return qs

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class PlacementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlacementPost.objects.all()
    serializer_class = PlacementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


urlpatterns = [
    path('placements/', PlacementListCreateAPIView.as_view(), name='api_placements'),
    path('placements/<int:pk>/', PlacementDetailAPIView.as_view(), name='api_placement_detail'),
]

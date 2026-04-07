from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserProfileSerializer
from .models import UserProfile


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            return UserProfile.objects.get(pk=pk)
        return self.request.user


urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('profile/', ProfileAPIView.as_view(), name='api_my_profile'),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='api_profile'),
]

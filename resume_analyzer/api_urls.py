from django.urls import path
from rest_framework import serializers, generics, permissions
from .models import ResumeAnalysis


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ['id', 'target_role', 'ats_score', 'analysis_result', 'suggestions', 'created_at']
        read_only_fields = ['id', 'ats_score', 'analysis_result', 'suggestions', 'created_at']


class AnalyzeResumeAPIView(generics.CreateAPIView):
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status
        from .utils import extract_text_from_file, analyze_resume_with_ai

        uploaded_file = request.FILES.get('resume_file')
        target_role = request.data.get('target_role', '')

        if not uploaded_file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        resume_text = extract_text_from_file(uploaded_file)
        uploaded_file.seek(0)
        analysis_data = analyze_resume_with_ai(resume_text, target_role)

        analysis = ResumeAnalysis.objects.create(
            user=request.user,
            resume_file=uploaded_file,
            target_role=target_role,
            ats_score=analysis_data.get('ats_score', 0),
            analysis_result=analysis_data,
            suggestions=analysis_data.get('suggestions', []),
        )

        serializer = self.get_serializer(analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


urlpatterns = [
    path('analyze-resume/', AnalyzeResumeAPIView.as_view(), name='api_analyze_resume'),
]

from rest_framework import serializers
from .models import UserProfile, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    profile_pic_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'full_name', 'email', 'user_type', 'branch',
                  'semester', 'graduation_year', 'current_company', 'current_role',
                  'bio', 'skills', 'profile_pic_url', 'github_url', 'linkedin_url',
                  'portfolio_url', 'is_verified', 'profile_completed']
        read_only_fields = ['id', 'username', 'user_type', 'is_verified']

    def get_profile_pic_url(self, obj):
        if obj.profile_pic:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_pic.url) if request else obj.profile_pic.url
        return None

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2',
                  'user_type', 'branch', 'semester', 'graduation_year']

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user

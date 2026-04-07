from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import UserProfile, Skill


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True, help_text='This will be used as your username')
    branch = forms.ChoiceField(choices=UserProfile.BRANCH_CHOICES)
    semester = forms.IntegerField(min_value=1, max_value=8, required=True)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'branch', 'semester')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            'email',
            Row(
                Column('branch', css_class='form-group col-md-8 mb-3'),
                Column('semester', css_class='form-group col-md-4 mb-3'),
            ),
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.user_type = 'student'
        if commit:
            user.save()
        return user


class AlumniRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True, help_text='This will be used as your username')
    branch = forms.ChoiceField(choices=UserProfile.BRANCH_CHOICES)
    graduation_year = forms.IntegerField(min_value=1990, max_value=2030, required=True)
    current_company = forms.CharField(max_length=200, required=False)
    current_role = forms.CharField(max_length=200, required=False)
    linkedin_url = forms.URLField(required=False, label='LinkedIn Profile Link', 
                                  widget=forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}))

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'branch',
                  'graduation_year', 'current_company', 'current_role', 'linkedin_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            'email',
            Row(
                Column('branch', css_class='form-group col-md-8 mb-3'),
                Column('graduation_year', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('current_company', css_class='form-group col-md-6 mb-3'),
                Column('current_role', css_class='form-group col-md-6 mb-3'),
            ),
            'linkedin_url',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.user_type = 'alumni'
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    skills_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Python, Django, React (comma separated)'
        }),
        help_text='Enter skills separated by commas'
    )

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'bio', 'branch', 'semester',
                  'graduation_year', 'current_company', 'current_role',
                  'profile_pic', 'resume', 'github_url', 'linkedin_url', 'portfolio_url']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'current_role': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must not exceed 5MB.')
            allowed_exts = ['.pdf', '.docx']
            ext = '.' + resume.name.rsplit('.', 1)[-1].lower()
            if ext not in allowed_exts:
                raise forms.ValidationError('Only PDF and DOCX files are allowed.')
        return resume

    def save(self, commit=True):
        user = super().save(commit=False)
        skills_text = self.cleaned_data.get('skills_input', '')
        if commit:
            user.save()
            if skills_text:
                user.skills.clear()
                for skill_name in [s.strip() for s in skills_text.split(',') if s.strip()]:
                    skill, _ = Skill.objects.get_or_create(name=skill_name.title())
                    user.skills.add(skill)
            user.profile_completed = True
            user.save()
        return user

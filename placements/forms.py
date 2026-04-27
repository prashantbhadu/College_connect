from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from accounts.models import UserProfile
from .models import PlacementPost, CompanyThread, PlacementRecord


class PlacementPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # We'll use the form tag in the template
        self.helper.layout = Layout(
            Row(
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                Column('role', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('role_type', css_class='form-group col-md-3 mb-0'),
                Column('ctc', css_class='form-group col-md-3 mb-0'),
                Column('min_cgpa', css_class='form-group col-md-3 mb-0'),
                Column('deadline', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'eligibility_criteria',
            'application_link',
            'description',
            'company_logo',
        )

    deadline = forms.DateField(
        input_formats=['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%m/%d/%Y'],
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = PlacementPost
        fields = ['company_name', 'role', 'role_type', 'ctc', 'min_cgpa', 'eligibility_criteria',
                  'deadline', 'application_link', 'description', 'company_logo']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Google'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer'}),
            'role_type': forms.Select(attrs={'class': 'form-select'}),
            'ctc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12 LPA'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.01, 'placeholder': 'e.g. 7.5'}),
            'eligibility_criteria': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'e.g. 7.5+ CGPA, B.Tech CSE/IT/ECE'
            }),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'application_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ThreadMessageForm(forms.ModelForm):
    class Meta:
        model = CompanyThread
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Ask a question or share your experience...'
            })
        }


class PlacementRecordForm(forms.ModelForm):
    class Meta:
        model = PlacementRecord
        fields = [
            'student', 'placement_post', 'company_name', 'role', 'role_type',
            'placement_status', 'placement_year', 'branch', 'package_lpa',
            'package_display', 'location', 'notes',
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'placement_post': forms.Select(attrs={'class': 'form-select'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Microsoft'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer'}),
            'role_type': forms.Select(attrs={'class': 'form-select'}),
            'placement_status': forms.Select(attrs={'class': 'form-select'}),
            'placement_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': 2100}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'package_lpa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01, 'placeholder': 'e.g. 12.50'}),
            'package_display': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12.5 LPA / 35K per month'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bengaluru'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional notes about the placement result'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = UserProfile.objects.filter(user_type='student').order_by('username')
        self.fields['placement_post'].queryset = PlacementPost.objects.order_by('-created_at')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('student', css_class='form-group col-md-6 mb-0'),
                Column('placement_post', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                Column('role', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('role_type', css_class='form-group col-md-3 mb-0'),
                Column('placement_status', css_class='form-group col-md-3 mb-0'),
                Column('placement_year', css_class='form-group col-md-3 mb-0'),
                Column('branch', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('package_lpa', css_class='form-group col-md-4 mb-0'),
                Column('package_display', css_class='form-group col-md-4 mb-0'),
                Column('location', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'notes',
        )

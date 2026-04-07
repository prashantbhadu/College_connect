from django import forms


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx'
        }),
        help_text='Upload your resume in PDF or DOCX format (max 5MB)'
    )
    target_role = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Software Engineer, Data Analyst, Product Manager'
        }),
        help_text='Enter the job role you are targeting for tailored keyword suggestions'
    )

    def clean_resume_file(self):
        f = self.cleaned_data.get('resume_file')
        if f:
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must not exceed 5MB.')
            name = f.name.lower()
            if not (name.endswith('.pdf') or name.endswith('.docx')):
                raise forms.ValidationError('Only PDF and DOCX files are accepted.')
        return f

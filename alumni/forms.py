from django import forms
from .models import AlumniPost, MentorshipRequest, AlumniQuery


class AlumniPostForm(forms.ModelForm):
    class Meta:
        model = AlumniPost
        fields = ['title', 'content', 'post_type', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Layout, Row, Column
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            Row(
                Column('post_type', css_class='form-group col-md-6 mb-3'),
                Column('tags', css_class='form-group col-md-6 mb-3'),
            ),
            'content',
        )


class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Introduce yourself and describe what guidance you are seeking...'
            })
        }


class AlumniQueryForm(forms.ModelForm):
    class Meta:
        model = AlumniQuery
        fields = ['question', 'is_public']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Layout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'question',
            'is_public',
        )


class QueryAnswerForm(forms.ModelForm):
    class Meta:
        model = AlumniQuery
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': 'Write your answer...'
            })
        }

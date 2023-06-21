from django import forms
from .models import Posts, Comments

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('body',)
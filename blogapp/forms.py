from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    encryption_type = forms.ChoiceField(choices=[('RSA', 'RSA'), ('Caesar', 'Caesar')])
    authorized_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'encryption_type', 'authorized_users']
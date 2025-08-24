from django import forms
from tinymce.widgets import TinyMCE
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


class PostForm(forms.ModelForm):
    body = forms.CharField(label="بدنه مقاله", widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))

    class Meta:
        model = Post
        fields = ["title", "image", "body", "slug", "is_premium"]
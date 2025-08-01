from django.shortcuts import render
from .models import Post


def home(request):
    posts = Post.objects.all()
    return render(request, "blogs/home.html", {'posts': posts})
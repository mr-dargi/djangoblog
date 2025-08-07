from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator


def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blogs/home.html", {'posts': page_obj})
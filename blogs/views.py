from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


def home(request):
    posts = Post.objects.filter(published=True)
    paginator = Paginator(posts, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blogs/home.html", {'posts': page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)

    return render(request, "blogs/post_detail.html", {"post": post})
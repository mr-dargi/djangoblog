from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator
from .forms import CommentForm


def home(request):
    posts = Post.objects.filter(published=True)
    paginator = Paginator(posts, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blogs/home.html", {'posts': page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(parent__isnull=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        parent_id = request.POST.get("parent_id")
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
            comment.save()
            return redirect("blogs:post_detail", slug=post.slug)
    else:
        form = CommentForm()

    return render(request, "blogs/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
        })
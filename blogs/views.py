from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages


def home(request):
    posts = Post.objects.filter(status="published")
    paginator = Paginator(posts, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blogs/home.html", {'posts': page_obj})


def post_detail(request, slug):
    """
    Display a blog post and handle comment actions.

    This view serves multiple purposes:
    - Show the post and its top-level comments.
    - Handle new comments and replies (via `parent_id`).
    - Handle editing existing comments (via `comment_id`).

    Keeping these actions in a single view makes sense because
    they all belong to the same post detail page. After each action,
    the user is redirected back to the same page for a seamless flow.
    """

    post = get_object_or_404(Post, slug=slug, status="published")
    comments = post.comments.filter(parent__isnull=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        parent_id = request.POST.get("parent_id")
        comment_id = request.POST.get("comment_id")
        if form.is_valid():
            if comment_id:
                comment = get_object_or_404(Comment, id=comment_id, post=post, user=request.user)
                print(comment)
                comment.body = form.cleaned_data["body"]
                comment.save()
            else:
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


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "کامنت شما با موفقیت حذف شد.", "success")
        return redirect("blogs:post_detail", slug=comment.post.slug)
    else:
        messages.error(request, "شما دارای دسترسی برای حذف این کامنت نیستید.", "danger")
        return redirect("blogs:post_detail", slug=comment.post.slug)
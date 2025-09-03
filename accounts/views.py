from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserLoginForm, UserRegistrationForm, PostForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from blogs.models import Post
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.db.models import Prefetch


def login_view(request):
    if request.user.is_authenticated:
        return redirect("blogs:home")
    
    
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["email"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید.", "success")
                return redirect("blogs:home")
            else:
                messages.error(request, "ایمیل یا پسورد وارد شده اشتباه می باشد.", "danger")
                return redirect("accounts:login")

    else:
        form = UserLoginForm()
       
    return render(request, "accounts/login.html", { "form": form })


def logout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "شما از قبل از حساب کاربری خود خارج شده اید.", "danger")
        return redirect("blogs:home")


    logout(request)
    messages.success(request, "شما با موفقیت از حساب خود خارج شدید.", "success")
    return redirect("blogs:home")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("blogs:home")
    

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(user_name=cd["username"], email=cd["email"], password=cd["password1"])
            messages.success(request, "شما با موفقیت ثبت نام کردید.", "success")
            return redirect("blogs:home")
    else:
        form = UserRegistrationForm()
    
    return render(request, "accounts/register.html", { "form": form })


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = "accounts/password_reset_form.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = "accounts/password_reset_email.html"


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


@login_required(login_url="/accounts/login/")
@role_required(["superuser", "author"])
def authorPage_view(request):
    posts = Post.objects.filter(author=request.user)
    
    return render(request, "accounts/authorPage.html", { "posts": posts })


@login_required(login_url="/accounts/login/")
@role_required(["superuser", "author"])
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = "draft"
            post.save()
            messages.success(request, 
                             "پست شما با موفقیت ذخیره شد پس از بررسی توسط ادمین ها منتشر می شود.",
                            "success"
                            )
            return redirect("accounts:create_post")
    else:
        form = PostForm()

    return render(request, "accounts/create_update_post.html", {"form":form})


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, "پست شما با موفقیت حذف شد.", "success")
        return redirect("accounts:authorPage")
    else:
        messages.error(request, "شما دارای دسترسی برای حذف این پست نیستید.", "danger")
        return redirect("blogs:home")


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        print(form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = "draft"
            post.save()
            messages.success(request, 
                             "پست شما با موفقیت ذخیره شد پس از بررسی توسط ادمین ها منتشر می شود.",
                            "success"
                            )
            return redirect("accounts:authorPage")
    else:
        form = PostForm(instance=post)
    
    return render(request, "accounts/create_update_post.html", {"form":form})


@login_required(login_url="/accounts/login/")
@role_required(["superuser", "admin"])
def admin_page(request):
    post_qs = Post.objects.only("id", "title", "status", "author_id").order_by("-created_at")
    authors = (
        User.objects
        .filter(post__isnull=False)
        .distinct()
        .prefetch_related(Prefetch("post_set", queryset=post_qs))
        .order_by("user_name")
    )

    return render(request, "accounts/adminPage.html", { "authors": authors })


@login_required(login_url="/accounts/login/")
@role_required(["superuser", "admin"])
def admin_post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Post.STATUS_CHOICES):
            post.status = new_status
            post.save()
        return redirect("accounts:admin_post_detail", post_id=post.id)
    
    return render(request, "accounts/admin_post_detail.html", {"post": post})


def profile(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=user)
    
    return render(request, "accounts/profile.html", { "form": form, "user": user })
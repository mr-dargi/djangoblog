from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserLoginForm, UserRegistrationForm, PostForm
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from blogs.models import Post
from django.contrib.auth.decorators import login_required
from .decorators import role_required


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
        print("1")
        form = PostForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print("2")
            post = form.save(commit=False)
            post.author = request.user
            post.status = "draft"
            post.save()
            messages.success(request, 
                             "پست شما با موفقیت ذخیره شد پس از بررسی توسط ادمین ها منتشر می شود.",
                            "success"
                            )
            return redirect("accounts:createPost", slug=post.slug)
    else:
        form = PostForm()

    return render(request, "accounts/create_post.html", {"form":form})
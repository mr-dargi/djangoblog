from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm
from django.contrib import messages


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
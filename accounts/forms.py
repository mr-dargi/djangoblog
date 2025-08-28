from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from blogs.models import Post
from tinymce.widgets import TinyMCE


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تایید رمز عبور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "user_name"]
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز ها با هم خوانایی ندارد")
        
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "user_name", "is_active", "is_admin", "role"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, label="ایمیل")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")


class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label="Password")
    password2 = forms.CharField(label="Confirm password")

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError("این ایمیل از قبل ثبت شده است.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(user_name=username).exists()

        if user:
            raise ValidationError("این نام کاربری ازقبل ثبت شده است.")
        return username

    
    def clean(self):
        cd = super().clean()
        p1 = cd.get("password1")
        p2 = cd.get("password2")

        if p1 and p2 and p2 != p2:
            raise ValidationError("رمز های عبور با هم تطابق ندارد.")


class PostForm(forms.ModelForm):
    body = forms.CharField(label="بدنه مقاله", widget=TinyMCE(attrs={'cols': 80, 'rows': 20, "class": "createPostTextarea",}))

    class Meta:
        model = Post
        fields = ["title", "image", "body", "slug", "is_premium"]
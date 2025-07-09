from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "user_name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["user_name"]}),
        ("Permissions", {"fields": ["is_admin"]})
    ]
    add_fieldsets = [
        (
            None, {
                    "classes": ["wide"],
                    "fields": ["email", "user_name", "password1", "password2"]
                }
        )
    ]


# Register UserAdmin
admin.site.register(User, UserAdmin)
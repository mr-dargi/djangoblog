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
    readonly_fields = ["last_login"]
    fieldsets = [
        ('Main', {'fields':('email', 'user_name', 'password')}),
        ("Permissions", {"fields": ["is_active", "is_admin", "is_superuser", "last_login", "groups", "user_permissions"]})
    ]
    add_fieldsets = [
        (
            None, {
                    "fields": ["email", "user_name", "password1", "password2"],
                }
        )
    ]
    search_fields = ["email", "user_name"]
    ordering = ["email"]
    filter_horizontal = ['groups', 'user_permissions']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fileds["is_superuser"].disabled = True
        return form


# Register UserAdmin
admin.site.register(User, UserAdmin)
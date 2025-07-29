from django.contrib.auth.decorators import user_passes_test


def role_required(role):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == role
    )
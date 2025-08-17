from django.urls import path, include
from .views import login_view


app_name = "accounts"
urlpatterns = [
    path("login/", login_view, name="login"),
]
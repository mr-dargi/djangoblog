from django.urls import path
from .views import home, post_detail


app_name = "blogs"
urlpatterns = [
    path("", home, name="home"),
    path("detail/<slug:slug>", post_detail, name="post_detail"),
]
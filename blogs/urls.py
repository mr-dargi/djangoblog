from django.urls import path
from . import views


app_name = "blogs"
urlpatterns = [
    path("", views.home, name="home"),
    path("detail/<slug:slug>", views.post_detail, name="post_detail"),
    path("createPost/", views.create_post, name="create_post"),
]
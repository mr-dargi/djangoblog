from django.urls import path
from . import views


app_name = "blogs"
urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.post_search, name="post_search"),
    path("about/", views.about, name="about"),
    path("detail/<slug:slug>", views.post_detail, name="post_detail"),
    path("comment/delete/<int:pk>/", views.delete_comment, name="delete_comment"),
    path("category/<slug:slug>/", views.category_list, name="category_list"),
]
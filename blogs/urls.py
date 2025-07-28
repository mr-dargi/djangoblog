from django.urls import path
from .views import home


app_name = "blogs"
urlpatterns = [
    path("", home, name="home"),
]
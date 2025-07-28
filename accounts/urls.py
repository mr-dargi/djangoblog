from django.urls import path, include
from .views import hello


app_name = "accounts"
urlpatterns = [
    path("", hello, name="hello"), # Just for solve a bug and later I will add views
]
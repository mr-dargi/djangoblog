from django.urls import path, include
from . import views


app_name = "accounts"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/",  views.register_view, name="register"),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
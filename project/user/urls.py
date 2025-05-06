from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

app_name='user'
urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),


]

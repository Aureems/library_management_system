from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import register_user, change_password, UserLogin, edit_profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password/', change_password, name='psw-change'),
    path('profile-update/', edit_profile, name='profile-update'),
]

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import register_user, login_user, logout_user
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
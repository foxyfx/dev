from django.contrib import admin
from django.urls import path , include 
from . import views


urlpatterns = [
    path('',views.home ,name="home"),
    path('login/',views.login_view ,name="login"),
    path('signup/',views.signup ,name="signup"),
    path('profile/',views.profile ,name="profile"),
    path('logout/',views.logout_view ,name="logout"),
    path('check_email/', views.check_email, name='check_email'),
]
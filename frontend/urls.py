from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    dashboard_page,
    profile_page,
    login_reg_page,
    movie_details_page
)
app_name = 'frontend'

urlpatterns = [
    path('movie/<int:movie_id>',movie_details_page,name='detail'),
    path('login',login_reg_page,name='login'),
    path('profile',profile_page,name='profile'),
    path('dashboard',dashboard_page,name='dashboard'),
    path('',TemplateView.as_view(template_name="pages/home.html")),
]

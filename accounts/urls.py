from django.urls import path
from .views import (
    login_view,
    logout_view,
    watched_movie,
    history
)
app_name = 'accounts'

urlpatterns = [
    path('login',login_view),
    path('logout',logout_view,name='log'),
    path('watch',watched_movie),
    path('watched',history),
]

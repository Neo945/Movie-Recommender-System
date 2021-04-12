from django.urls import path
from django.views.generic.base import TemplateView
app_name = 'frontend'

urlpatterns = [
    path('',TemplateView.as_view(template_name="pages/auth.html")),
    # path('',TemplateView.as_view(template_name="pages/profile.html")),
]

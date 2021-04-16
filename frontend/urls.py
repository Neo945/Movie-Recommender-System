from django.urls import path
from django.views.generic.base import TemplateView
app_name = 'frontend'

urlpatterns = [
    path('movie/<int:i>',TemplateView.as_view(template_name="pages/details.html")),
    path('',TemplateView.as_view(template_name="pages/dashboard.html")),
]

from django.contrib.auth.models import User
from django.core.exceptions import RequestDataTooBig
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

# Create your views here.
def login_view(request):
    form = AuthenticationForm(request,request.user or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request,user_)
        redirect('/')

def logout_view(request):
    logout(request)
    redirect('/')

def register_view(request):
    form = UserCreationForm(request.user or None)
    if form.is_valid():
        u = form.save(commit=True)
        redirect('/')
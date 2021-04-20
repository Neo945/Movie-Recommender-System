from accounts.models import History, Profile
from django.shortcuts import redirect, render
from movies.models import Movie
from movies.serializers import MovieSerializer

# Create your views here.
def login_reg_page(request):
    if request.user and request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request,'pages/auth.html',{})
    
def dashboard_page(request):
    if not request.user and request.user.is_authenticated:
        return redirect('/login')
    return render(request,'pages/dashboard.html',{})

def movie_details_page(request,movie_id):
    qs = Movie.objects.filter(pk=movie_id)
    if qs.exists():
        return render(request,'pages/details.html',{'data':MovieSerializer(qs.first()).data},status=200)
    return render(request,'pages/404.html',{'data':'movie not found'},status=404)

def profile_page(request):
    count = History.objects.filter(user=Profile.objects.filter(user= request.user).first()).count()
    print(request.user.email)
    return render(request,'pages/profile.html',{'data':{'count':count},},status=200)
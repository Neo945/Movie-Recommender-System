from accounts.serializers import HistoryCreateSerializer, HistorySerializer
from movies.models import Movie
from accounts.models import History, Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
def login_view(request):
    form = AuthenticationForm(request,request.user or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request,user_)
        return redirect('/')
    return render('auth/form.html',{'form':form})

@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.user:
        logout(request)
        return redirect('/login')
    return redirect('/login')

def register_view(request):
    form = UserCreationForm(request.user or None)
    if form.is_valid():
        u = form.save(commit=True)
        Profile(user=u).save()
        return redirect('/')
    return render('auth/form.html',{'form':form})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def watched_movie(request):
    serial = HistoryCreateSerializer(data=request.data or None)
    if serial.is_valid():
        serial.save(user=Profile.objects.filter(user=request.user).first())
        return Response({'message':f'Enjoy your movie'},status=201)
    return Response({'message':'Movie doesnot exists'},status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    qs = History.objects.filter(user=Profile.objects.filter(user=request.user).first())
    return Response(HistorySerializer(qs,many=True).data,status=200)
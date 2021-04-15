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
    if request.user.is_authenticated and request.user:
        print(request.user)
        return redirect('/')
    if request.method=='POST':
        if request.POST.get('login')=='1':
            form = AuthenticationForm(request,data=request.POST or None)
            if form.is_valid():
                user_ = form.get_user()
                login(request,user_)
                return redirect('/')
        else:
            form = UserCreationForm(request.POST or None)
            if form.is_valid():
                print('qwerty')
                u = form.save(commit=True)
                Profile(user=u).save()
                return redirect('/')
    return render(request,'pages/auth.html',{})

@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.user:
        logout(request)
        return redirect('/login')
    return redirect('/login')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def watched_movie(request):
    serial = HistoryCreateSerializer(data=request.data or None)
    if serial.is_valid():
        serial.save(user=Profile.objects.filter(user=request.user).first())
        return Response({'message':f'Enjoy your movie'},status=201)
    return Response({'message':'Movie doesnot exists'},status=404)
"""
{
"movies":1,
"user_rating":4,
"comments":"qwerty"
}
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    qs = History.objects.filter(user=Profile.objects.filter(user=request.user).first())
    return Response(HistorySerializer(qs,many=True).data,status=200)
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import *
from .forms import NewUserForm
from django.contrib.auth import login,logout
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
@login_required()
def home(request):
    return redirect('homeclinic')


def customeLogout(request):
    logout(request)
    return redirect('Goodbye')

def bye(request):
    if request.user.is_authenticated:
        current_user = request.user
        return render(request,'logout_first.html',{'user':current_user})
    return render(request,'exit.html',{})

def welcome(request):
    if request.user.is_authenticated:
        current_user = request.user
        return render(request,'logout_first.html',{'user':current_user})
    return render(request,'welcome.html')


def register_request(request):
    if request.user.is_authenticated:
        current_user = request.user
        return render(request,'logout_first.html',{'user':current_user})
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('registerpage')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('registerpage')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('registerpage')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('registerpage')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('registerpage')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        return redirect('baselogin')
    return render(request, "register.html")



class test_form12(CreateView):
    model = User
    fields = ('username','password')
    template_name = 'forms_tests.html'
    def get_success_url(self):
        return reverse('home')
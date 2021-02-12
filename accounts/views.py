from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import SignUpForm


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    
    
class Logout(LogoutView):
    template_name = 'accounts/logout.html'


class Signup(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('profiles:index')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

   
    
    
    
    
    

    
        
            
        

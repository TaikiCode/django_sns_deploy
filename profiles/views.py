from django.shortcuts import render

from .models import Profile

def index(request):
    profile = Profile.objects.all()
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'profiles/index.html', context)

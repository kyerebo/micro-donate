from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render

def index(request):
    return HttpResponse("You're Looking at a functioning Django Page")

def check(request):
    if(request.user.is_authenticated):
        for p in Profile.objects.all():
            if(p.user_name == request.user.username):
                return HttpResponseRedirect(reverse('dashboard'))
        acc = Profile.objects.create(user_name = request.user.username, account = request.user, xp = 0)
        acc.save()
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseRedirect(reverse('mainlogin'))
                
        
def profile(request):
    levels = [0, 1000, 2000, 3500, 5000, 6750, 8500, 10000]
    prof = None
    if(request.user.is_authenticated):
        for p in Profile.objects.all():
            if(p.user_name == request.user.username):
                prof = p
        for idx, exp in enumerate(levels):
            if prof.xp >= exp:
                level = idx
        if level==len(levels)-1:
            percentage = 100
            needed = 0
        else:
            percentage = int(100*(prof.xp-levels[level])/(levels[level+1]-levels[level]))
            needed = levels[level + 1] - prof.xp
        return render(request, 'microdonate/profile.html', {
            'level': level,
            'percent' : percentage,
            'xp' : prof.xp,
            'needed' : needed
        })
    else:
        return HttpResponseRedirect(reverse('mainlogin'))
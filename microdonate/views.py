from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
def index(request):
    user = request.user
    context = {'user' : user}
    return render(request, 'microdonate/dash.html', context)

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
                
        

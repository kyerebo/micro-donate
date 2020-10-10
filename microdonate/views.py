from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
def index(request):
    return HttpResponse("You're Looking at a functioning Django Page")

def usercheck(request):
    if(request.user.is_authenticated):
        for p in Profile.objects.all():
            if(p.user_name == request.user.username):
                return HttpResponseRedirect(reverse('microdonate:dashboard'))
        acc = Profile.objects.create(user_name = request.user.username, account = request.user, xp = 0)
        acc.save()
        return HttpResponseRedirect(reverse('microdonate:dashboard'))
    else:
        return HttpResponseRedirect(reverse('microdonate:login'))
                
        

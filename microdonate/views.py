from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, Volunteer, Donate
def index(request):
    levels = [0,1000,2000,3500,5000,6750,8500,10000]

    prof = None
    for p in Profile.objects.all():
        if(p.user_name == request.user.username):
            prof = p

    prof.xp = 7492

    level = 0
    for idx,exp in enumerate(levels):
        if prof.xp >= exp:
            level = idx
    
    if level==len(levels)-1:
        percentage = 100
        needed = 0
    else:
        percentage = int(100*(prof.xp-levels[level])/(levels[level+1]-levels[level]))
        needed = levels[level+1] - prof.xp

    user = request.user
    context = {
        'level' : level,
        'percent' : percentage,
        'xp' : prof.xp,
        'needed' : needed,
        'user' : user
    }
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
        volunteers = list()
        for v in Volunteer.objects.filter(volunteer_users=prof):
            volunteers.append(v)
        donates = list()
        for d in Donate.objects.filter(donate_users=prof):
            donates.append(d)
        return render(request, 'microdonate/profile.html', {
            'level': level,
            'percent' : percentage,
            'xp' : prof.xp,
            'needed' : needed,
            'Volunteers' : volunteers,
            'Donates' : donates
        })
    else:
        return HttpResponseRedirect(reverse('mainlogin'))

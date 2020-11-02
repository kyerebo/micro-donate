from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import loader
from django.utils import timezone
from .models import Profile, Volunteer, Donate, Comments
def index(request):
    levels = [0,1000,2000,3500,5000,6750,8500,10000]

    prof = None
    for p in Profile.objects.all():
        if(p.user_name == request.user.username):
            prof = p

    if prof!=None:
        prof.xp = 7492
    else:
        prof = Profile.objects.create(user_name='Test Account',xp=3742)

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
    # temp_names = ['name 1','name 2','name 3']
    # temp_orgs = ['org 1', 'org 2', 'org 3']
    # temp_goals = [100, 200, 300]
    # temp_descriptions = ['description 1', 'description 2', 'description 3']
    # # the next 3 lines are temp
    # Volunteer.objects.all().delete()
    # for i in range(len(temp_names)):
    #     Volunteer.objects.create(volunteer_name=temp_names[i], organization_name=temp_orgs[i], goal=temp_goals[i], description=temp_descriptions[i])
    volunteer = Volunteer.objects.all()
    # # the next 3 lines are temp
    # Donate.objects.all().delete()
    # for i in range(len(temp_names)):
    #     Donate.objects.create(donate_name=temp_names[i], organization_name=temp_orgs[i], goal=temp_goals[i], description=temp_descriptions[i])
    donate = Donate.objects.all()
    context = {
        'level' : level,
        'percent' : percentage,
        'xp' : prof.xp,
        'needed' : needed,
        'user' : user,
        'volunteer' : volunteer,
        'donate' : donate
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

def comments(request):
    comments = Comments.objects.all()
    temp = loader.get_template('microdonate/comments.html')

    context = {
        'comments': comments
    }

    return HttpResponse(temp.render(context,request))

def submit(request):
    left_comment = Comments(comments_title='',comments_text='',pub_date=timezone.now())
    left_comment.comments_title = request.POST.get('comments_title', False)
    left_comment.comments_text = request.POST.get('comments_text', False)
    left_comment.save()
    return HttpResponseRedirect('list')

def comments_list(request):
    comments = Comments.objects.all()
    context = {
        'comments': comments
    }

    return HttpResponse(loader.get_template('microdonate/comments_list.html').render(context,request))

def detVol(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    isSignedUp = False
    for u in op.volunteer_users.all():
        if(u.user_name == request.user.username):
            isSignedUp = True
    return render(request, 'microdonate/detailVol.html', {
        'op' : op,
        'title' : op.volunteer_name,
        'signedup' : isSignedUp,
        'profs' : op.volunteer_users.all()
    })

def detDon(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
    return render(request, 'microdonate/detailDon.html', {
        'op' : op,
    })
def submitDonation(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
    #do payment stuff here
    #need to find a way to push donation amount through this into donation confirmation page
    return HttpResponseRedirect(reverse('confirmDonation', args=(opp_id, )))
def confirmDonation(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
    name = op.donate_name
    return HttpResponse("You just donated to: " + name)
def signup(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    p = Profile.objects.get(pk=1)
    for prof in Profile.objects.all():
        if(request.user.username == prof.user_name):
            p = prof
    op.volunteer_users.add(p)
    return HttpResponseRedirect(reverse('signUpConfirm', args=(opp_id, )))
def confirmation(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    return render(request, 'microdonate/confirmsignup.html', {
        'op' : op,
        'user' : request.user,
    })

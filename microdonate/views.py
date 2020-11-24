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

    if prof==None:
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
    volunteer = Volunteer.objects.all()
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
        for d in Donate.objects.all():
            if(prof in d.donate_users.all()):
                donates.append(d)
        return render(request, 'microdonate/profile.html', {
            'level': level,
            'percent' : percentage,
            'xp' : prof.xp,
            'needed' : needed,
            'Volunteers' : volunteers,
            'Donations' : donates
        })
    else:
        return HttpResponseRedirect(reverse('mainlogin'))

def donate_comments(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
    comments = op.comments
    temp = loader.get_template('microdonate/donate_comments.html')

    context = {
        'op': op,
        'comments': comments,
        'opp_id' : opp_id
    }

    return HttpResponse(temp.render(context,request))

def donate_submit(request, opp_id):
    # temp = opp_id
    op = Donate.objects.get(pk=opp_id)
    left_comment = Comments(comments_title='',comments_text='',pub_date=timezone.now())
    title = request.POST.get('comments_title', '<No Title>')
    text = request.POST.get('comments_text', '<No Body>')
    left_comment.comments_title = title if title else '<No Title>'
    left_comment.comments_text = text if text else '<No Title>'
    left_comment.save()
    op.comments.add(left_comment)
    return HttpResponseRedirect('list')

def donate_comments_list(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
    comments = op.comments.all()
    context = {
        'op': op,
        'comments': comments,
        'opp_id' : opp_id
    }

    return HttpResponse(loader.get_template('microdonate/donate_comments_list.html').render(context,request))

def volunteer_comments(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    comments = op.comments
    temp = loader.get_template('microdonate/volunteer_comments.html')

    context = {
        'op': op,
        'comments': comments,
        'opp_id' : opp_id
    }

    return HttpResponse(temp.render(context,request))

def volunteer_submit(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    left_comment = Comments(comments_title='',comments_text='',pub_date=timezone.now())
    title = request.POST.get('comments_title', '<No Title>')
    text = request.POST.get('comments_text', '<No Body>')
    left_comment.comments_title = title if title else '<No Title>'
    left_comment.comments_text = text if text else '<No Title>'
    left_comment.save()
    op.comments.add(left_comment)
    return HttpResponseRedirect('list')

def volunteer_comments_list(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    comments = op.comments.all()
    context = {
        'op': op,
        'comments': comments,
        'opp_id' : opp_id
    }

    return HttpResponse(loader.get_template('microdonate/volunteer_comments_list.html').render(context,request))

def detVol(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    isSignedUp = False
    for u in op.volunteer_users.all():
        if(u.user_name == request.user.username):
            isSignedUp = True
    locateString = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCeJcdX1DHrCnHcZOrQ9duEp2MFEw5I7eU&q=" + op.location
    return render(request, 'microdonate/detailVol.html', {
        'op' : op,
        'title' : op.volunteer_name,
        'signedup' : isSignedUp,
        'profs' : op.volunteer_users.all(),
        'loc' : locateString,
        'opp_id' : opp_id
    })

def detDon(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
    return render(request, 'microdonate/detailDon.html', {
        'op' : op,
        'profs' : op.donate_users.all(),
        'opp_id' : opp_id
    })
def about(request):
    return render(request, 'microdonate/about.html', {
        'user' : request.user,
    })
def leaderboard(request):
    prof = Profile.objects.get(user_name= request.user.username)
    board = Profile.objects.all().order_by('-xp')
    user = request.user
    return render(request, 'microdonate/leaderboard.html', {
        'board' : board,
        'prof' : prof,
        'user' : user,
    })
def submitDonation(request, opp_id):
    op = Donate.objects.get(pk=opp_id)
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
    p.xp += 200
    op.volunteer_users.add(p)
    p.save()
    return HttpResponseRedirect(reverse('signUpConfirm', args=(opp_id, )))
def confirmation(request, opp_id):
    op = Volunteer.objects.get(pk=opp_id)
    return render(request, 'microdonate/confirmsignup.html', {
        'op' : op,
        'user' : request.user,
    })

def update_xp(request):
    username = request.GET.get('user')
    donation_amount = float(request.GET.get('donation'))
    donation = request.GET.get('opp')
    for prof in Profile.objects.all():
        if(username == prof.user_name):
            p = prof
            break
    dona = None
    for don in Donate.objects.all():
        if( don.donate_name == donation):
            dona = don
            break
    if dona!=None:
        dona.donate_users.add(p)
    p.xp += int(donation_amount*50)
    p.save()
    return HttpResponseRedirect(reverse('dashboard'))
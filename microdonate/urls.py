"""microdonate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import TemplateView
from . import views

app_name = 'microdonate'
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', TemplateView.as_view(template_name="microdonate/google.html"), name = "login"),
    path('usercheck/', views.check, name="usercheck"),
    path('dash/', views.index, name="dashboard"),
    path('accounts/', include('allauth.urls'), name="accounts"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name='about'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('update_xp/', views.update_xp, name='update_xp'),
    path('donate/<int:opp_id>/comments/submit/list', views.donate_comments_list, name='donate_comments_list'),
    path('donate/<int:opp_id>/comments/submit/', views.donate_submit, name='donate_submit'),
    path('donate/<int:opp_id>/comments/', views.donate_comments, name='donate_comments'),
    path('donate/<int:opp_id>/', views.detDon, name='detDon'),
    path('donate/<int:opp_id>/pay/', views.submitDonation, name='submitDonation'),
    path('donate/<int:opp_id>/confirm/', views.confirmDonation, name='confirmDonation'),
    path('volunteer/<int:opp_id>/comments/submit/list', views.volunteer_comments_list, name='volunteer_comments_list'),
    path('volunteer/<int:opp_id>/comments/submit/', views.volunteer_submit, name='volunteer_submit'),
    path('volunteer/<int:opp_id>/comments/', views.volunteer_comments, name='volunteer_comments'),
    path('volunteer/<int:opp_id>/', views.detVol, name='detVol'),
    path('volunteer/<int:opp_id>/confirm/', views.confirmation, name='signUpConfirm'),
    path('volunteer/<int:opp_id>/signup/', views.signup, name='signup'),
]

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Profile, Volunteer, Donate

# add imports and test cases

class TravisTesting(TestCase):

    # check if travis works
    def test_always_passing_test(self):
        self.assertTrue(True)
    def test_one_plus_one(self):
        self.assertEqual(2,1+1)

class ProgressBarTesting(TestCase):
    def test_percentage_accurate(self):
        prof = Profile.objects.create(account=None, user_name="me", xp=450)
        levels = [0,1000,2000,3500,5000,6750,8500,10000]
        for idx,exp in enumerate(levels):
            if prof.xp >= exp:
                level = idx
        if level==len(levels)-1:
            percentage = 100
            needed = 0
        else:
            percentage = int(100*(prof.xp-levels[level])/(levels[level+1]-levels[level]))
            needed = levels[level+1] - prof.xp
        self.assertEqual(percentage, 45)
            
    def test_level_accurate(self):
        prof = Profile.objects.create(account=None, user_name="me", xp=4500) #level 3
        levels = [0,1000,2000,3500,5000,6750,8500,10000]
        level = 0
        for idx,exp in enumerate(levels):
            if prof.xp >= exp:
                level = idx
        self.assertEqual(level,3)
    
    def test_level_case(self):
        prof = Profile.objects.create(account=None, user_name="me", xp=10000) #level 7 (maxed)
        levels = [0,1000,2000,3500,5000,6750,8500,10000]
        level = 0
        for idx,exp in enumerate(levels):
            if prof.xp >= exp:
                level = idx
        self.assertEqual(level,7)

    def test_level_edge_case(self):
        prof = Profile.objects.create(account=None, user_name="me", xp=12000) #level 7 (maxed)
        levels = [0,1000,2000,3500,5000,6750,8500,10000]
        level = 0
        for idx,exp in enumerate(levels):
            if prof.xp >= exp:
                level = idx
        self.assertEqual(level,7)
    
    def test_level_edge_case2(self):
        prof = Profile.objects.create(account=None, user_name="me", xp=0) #level 0
        levels = [0,1000,2000,3500,5000,6750,8500,10000]
        level = 0
        for idx,exp in enumerate(levels):
            if prof.xp >= exp:
                level = idx
        self.assertEqual(level,0)

        
class ProfileTesting(TestCase):
    def test_new_profile_username(self):
        prof = Profile.objects.create(account=None, user_name="new profile", xp=0)
        self.assertEqual("new profile", prof.user_name)

class VolunteerTesting(TestCase):
    def test_new_volunteer(self):
        v = Volunteer.objects.create(volunteer_name="test_name")
        self.assertEqual("test_name",v.volunteer_name)
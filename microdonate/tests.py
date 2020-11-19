import datetime

from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Profile, Volunteer, Donate, Comments
from .views import signup

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
    
    def test_volunteer_users(self):
        v = Volunteer.objects.create(volunteer_name="testing")
        p = Profile.objects.create(account=None, user_name="hello")
        v.volunteer_users.add(p)
        self.assertIn(p, v.volunteer_users.all())
    
    def test_check_display(self):
        v = Volunteer.objects.create(volunteer_name="testing123")
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "testing123")

class DonateTesting(TestCase):
    def test_new_donate(self):
        d = Donate.objects.create(donate_name="test_name")
        self.assertEqual("test_name",d.donate_name)
    
    def test_donate_users(self):
        d = Donate.objects.create(donate_name="testing")
        p = Profile.objects.create(account=None, user_name="user")
        d.donate_users.add(p)
        self.assertIn(p, d.donate_users.all())
    
    def test_check_display(self):
        d = Donate.objects.create(donate_name="testing123")
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "testing123")

class CommentsTesting(TestCase):
    def test_blank_body(self):
        c = Comments.objects.create()
        self.assertEqual(c.comments_text,'<No Body>')
    
    def test_blank_title(self):
        c = Comments.objects.create()
        self.assertEqual(c.comments_title,'<No Title>')
    
    def test_body(self):
        c = Comments.objects.create(comments_text='test text')
        self.assertEqual(c.comments_text,'test text')
    
    def test_title(self):
        c = Comments.objects.create(comments_title='test title')
        self.assertEqual(c.comments_title,'test title')

# class leaderboardTest(TestCase):
    #def test_leaderboard(self):
        #a = Profile.objects.create(account=None, user_name="qwerty", xp=200)
        #b = Profile.objects.create(account=None, user_name="b", xp=350)
        #response = self.client.get(reverse('leaderboard'))
        #self.assertContains(response, "qwerty")
        

class XPUpdateTest(TestCase):
    def test_donate_xp(self):
        p = Profile.objects.create(account=None, user_name="hello",xp=123)
        response = self.client.get('/update_xp/',{"donation":"10.0","user":"hello"})
        p.refresh_from_db()
        self.assertEqual(p.xp, 123+int(10.0*50))

    def test_donate_xp_large(self):
        p = Profile.objects.create(account=None, user_name="hello2",xp=1234)
        response = self.client.get('/update_xp/',{"donation":"100000.0","user":"hello2"})
        p.refresh_from_db()
        self.assertEqual(p.xp, 1234+int(100000.0*50))

    def test_donate_xp_fraction(self):
        p = Profile.objects.create(account=None, user_name="hello",xp=34)
        response = self.client.get('/update_xp/',{"donation":"1000.50","user":"hello"})
        p.refresh_from_db()
        self.assertEqual(p.xp, 34+int(1000.50*50))

    def test_donate_xp_0(self):
        p = Profile.objects.create(account=None, user_name="hello",xp=3244)
        response = self.client.get('/update_xp/',{"donation":"0.0","user":"hello"})
        p.refresh_from_db()
        self.assertEqual(p.xp, 3244+int(0*50))
        
    def test_volunteer_xp(self):
        p = Profile.objects.create(account=None, user_name="hello",xp=123)
        v = Volunteer.objects.create(volunteer_name="testing123")
        fac = RequestFactory()
        request = fac.get('/volunteer/signup/')
        class User:
            username = "hello"
        request.user = User()
        response = signup(request,1)
        p.refresh_from_db()
        v.refresh_from_db()
        self.assertEqual(p.xp,123+200)
        self.assertIn(p, v.volunteer_users.all())
    
    def test_volunteer_xp_twice(self):
        p = Profile.objects.create(account=None, user_name="hello",xp=123)
        v = Volunteer.objects.create(volunteer_name="testing123")
        v2 = Volunteer.objects.create(volunteer_name="testing1234")
        fac = RequestFactory()
        request = fac.get('/volunteer/signup/')
        class User:
            username = "hello"
        request.user = User()
        response = signup(request,1)

        fac = RequestFactory()
        request = fac.get('/volunteer/signup/')
        request.user = User()
        response = signup(request,2)

        p.refresh_from_db()
        v.refresh_from_db()
        v2.refresh_from_db()
        self.assertEqual(p.xp,123+200+200)
        self.assertIn(p, v.volunteer_users.all())
        self.assertIn(p, v2.volunteer_users.all())

    def test_volunteer_xp_three(self):
        p = Profile.objects.create(account=None, user_name="hello",xp=123)
        p2 = Profile.objects.create(account=None, user_name="hello2",xp=12345)
        v = Volunteer.objects.create(volunteer_name="testing123")

        fac = RequestFactory()
        request = fac.get('/volunteer/signup/')
        class User:
            username = "hello"
        request.user = User()
        response = signup(request,1)

        temp = User()
        temp.username = "hello2"

        fac = RequestFactory()
        request = fac.get('/volunteer/signup/')
        request.user = temp
        response = signup(request,1)

        p.refresh_from_db()
        p2.refresh_from_db()
        self.assertEqual(p.xp,123+200)
        self.assertEqual(p2.xp,12345+200)
        self.assertIn(p, v.volunteer_users.all())
        self.assertIn(p2, v.volunteer_users.all())
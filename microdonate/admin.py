from django.contrib import admin

from .models import Profile, Donate, Volunteer, Comments

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user_name', 'xp')
        }),
    )
    list_display = ('user_name','xp')
    list_filter = ['user_name']
    search_fields = ['user_name']

class DonateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['organization_name','donate_name','description','goal','donate_amount','donate_users']
        }),
    )
    list_display = ('organization_name','donate_name','get_users')
    list_filter = ['organization_name','donate_name']

    def get_users(self, obj):
        return "\n".join([p.user_name for p in obj.donate_users.all()])

class VolunteerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['organization_name','volunteer_name','date','location','goal','description','volunteer_users']}),
    )
    list_display = ('organization_name','volunteer_name','date','get_users')
    list_filter = ['organization_name','volunteer_name','date','location']
    search_fields = ['organization_name','volunteer_name']

    def get_users(self, obj):
        return "\n".join([p.user_name for p in obj.volunteer_users.all()])

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Donate, DonateAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
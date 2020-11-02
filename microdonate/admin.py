from django.contrib import admin

from .models import Profile, Donate, Volunteer, Comments

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user_name', 'xp')
        }),
    )
    list_display = ('user_name','xp')
    list_filter = ['user_name','xp']
    search_fields = ['user_name']

class DonateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['donate_name','donate_users']
        }),
    )
    list_display = ('donate_name','get_users')
    list_filter = ['donate_name']

    def get_users(self, obj):
        return "\n".join([p.user_name for p in obj.donate_users.all()])

class VolunteerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['volunteer_name','organization_name','goal','description','volunteer_users']}),
    )
    list_display = ('volunteer_name','get_users')
    list_filter = ['volunteer_name','organization_name']
    search_fields = ['volunteer_name','organization_name']

    def get_users(self, obj):
        return "\n".join([p.user_name for p in obj.volunteer_users.all()])

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Donate, DonateAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
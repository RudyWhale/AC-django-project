from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class UserSettingsInline(admin.StackedInline):
    model = UserSettings


class ACUserAdmin(UserAdmin):
    inlines = [UserSettingsInline, ]


admin.site.unregister(User)
admin.site.register(User, ACUserAdmin)

admin.site.register(ArtworkCategory)
admin.site.register(Artwork)
admin.site.register(ArtistProfile)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Publication)
admin.site.register(FeedUpdateEmailTask)
admin.site.register(BlackList)
admin.site.register(SubscriberWebNotification)

from django.contrib import admin
from .models import Artwork, ArtistProfile, Comment, Tag, Publication

admin.site.register(Artwork)
admin.site.register(ArtistProfile)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Publication)

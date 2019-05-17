from django.contrib import admin
from .models import Artwork, Article, ArtistProfile, Comment, Tag;

admin.site.register(Artwork)
admin.site.register(Article)
admin.site.register(ArtistProfile)
admin.site.register(Comment)
admin.site.register(Tag)

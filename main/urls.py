from django.urls import path, re_path, include
from django.conf.urls.static import static
from . import views
from ArtChart import settings

urlpatterns = [
	path('', views.index, name='index'),
	path(
		'main',
		views.index,
		name='index'
	),
	path(
		'artists',
		views.artists,
		name='artists'
		),
	path(
		'artist/<int:pk>',
		views.artist,
		name='artist'
	),
	path(
		'artworks',
		views.artworks,
		name='artworks'
	),
	path(
		'artworks/<int:pk>',
		views.artwork,
		name='artwork'
	),
	path(
		'tag/<int:pk>',
		views.tag,
		name='tag'
	),
	path(
		'become_artist',
		views.become_artist,
		name='become artist'
	),
	path(
		'feed',
		views.feed,
		name='feed'
	)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

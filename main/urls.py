from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect
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
		'feed',
		views.feed,
		name='feed'
	),
	path(
		'feedback',
		views.feedback,
		name='feedback'
	),
	path(
		'robots.txt',
		views.robots,
		name ='robots'
	),
    path(
        'new_artwork',
        views.new_artwork,
        name='new artwork'
    ),
	path(
		'settings',
		views.settings,
		name='settings'
	),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, re_path, include
from django.conf.urls.static import static
from . import views, ajax
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
	),
	path(
		'load_content_publications',
		ajax.load_content_publications,
		name='load content publications'
	),
	path(
		'load_content_tag/<int:pk>',
		ajax.load_content_tag,
		name='load content tag'
	),
	path(
		'load_content_feed',
		ajax.load_content_feed,
		name='load content feed'
	),
	path(
		'load_content_main',
		ajax.load_content_main,
		name='load content main'
	),
	path(
		'load_content_artist/<int:pk>',
		ajax.load_content_artist,
		name='load content artist'
	)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

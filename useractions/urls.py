from django.urls import path, re_path, include
from . import views
from django.conf.urls.static import static
from ArtChart import settings

urlpatterns = [
	path('like', views.like, name='like'),
	path('subscribe', views.subscribe, name='subscribe'),
	path('comment', views.comment, name='comment'),
	path(
		'load_content_publications',
		views.load_content_publications,
		name='load content publications'
	),
	path(
		'load_content_tag/<int:pk>',
		views.load_content_tag,
		name='load content tag'
	),
	path(
		'load_content_feed',
		views.load_content_feed,
		name='load content feed'
	),
	path(
		'views',
		views.load_content_main,
		name='load content main'
	),
	path(
		'load_content_artist/<int:pk>',
		views.load_content_artist,
		name='load content artist'
	)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

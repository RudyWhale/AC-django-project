from django.urls import path, re_path, include
from . import views
from django.conf.urls.static import static
from ArtChart import settings

urlpatterns = [
	path(
		'like',
		views.like,
		name='like'
	),
	path(
		'subscribe',
		views.subscribe,
		name='subscribe'
	),
	path(
		'comment',
		views.comment,
		name='comment'
	),
	path(
		'reply',
		views.reply,
		name='reply'
	),
	path(
		'load_content_category/<int:pk>',
		views.load_content_category,
		name='load content category'
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
		'load_content_main',
		views.load_content_main,
		name='load content main'
	),
	path(
		'load_content_artist/<int:pk>',
		views.load_content_artist,
		name='load content artist'
	),
	path(
		'load_artist_profiles',
		views.load_artist_profiles,
		name='load artist profiles'
	),
	path(
		'delete_comment/<int:pk>',
		views.delete_comment,
		name='delete comment'
	),
	path(
		'delete_reply/<int:pk>',
		views.delete_reply,
		name='delete reply'
	),
	path(
		'delete_publication/<int:pk>',
		views.delete_publication,
		name='delete publication'
	),
	path(
		'clear_notifications',
		views.clear_notifications,
		name='clear notifications'
	),
	path(
		'logout',
		views.logout,
		name='logout'
	),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

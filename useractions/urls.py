from django.urls import path, re_path, include
from . import views
from django.conf.urls.static import static
from ArtChart import settings

urlpatterns = [
	path('like', views.like, name='like'),
	path('subscribe', views.subscribe, name='subscribe'),
	path('comment', views.comment, name='comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

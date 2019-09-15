from django.urls import path
from django.conf.urls.static import static
from ArtChart import settings
from . import views

urlpatterns = [
    path(
        'new-artwork',
        views.new_artwork,
        name='new-artwork'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

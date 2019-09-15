from django.http import HttpResponse
from datetime import datetime
import json
from .models import Artwork, Tag, Publication
from ArtChart.settings import CONTENT_ITEMS_LIMIT as LIMIT

def get_content(query, from_date):
    query = query.exclude(datetime__lt = from_date)[:LIMIT]
    content = ''.join([obj.as_html() for obj in query])
    return HttpResponse(content)


def load_content_publications(request):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    query = Artwork.objects.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + LIMIT]
    shown = int(request.GET['shown'])
    content = ''.join([obj.as_html() for obj in query])
    return HttpResponse(content)


def load_content_tag(request, pk):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Tag.objects.get(pk = pk).publications.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    return HttpResponse(content)


def load_content_feed(request):
    if request.user.is_authenticated:
        publications = Publication.objects.none()
        from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
        for artistprofile in request.user.subscriptions.all():
        	publications = publications.union(artistprofile.publication_set.exclude(datetime__gt = from_date).all())

        from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
        shown = int(request.GET['shown'])
        query = publications.order_by('-datetime')[shown:shown + LIMIT]
        content = ''.join([obj.artwork.as_html() for obj in query])
        return HttpResponse(content)

    else:
        return HttpResponse('Произошла ошибка')

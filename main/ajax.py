from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from datetime import datetime
import json
from .models import Artwork, Tag, Publication, ArtistProfile
from ArtChart.settings import CONTENT_ITEMS_LIMIT as LIMIT

# def get_content(query, from_date):
#     query = query.exclude(datetime__lt = from_date)[:LIMIT]
#     content = ''.join([obj.as_html() for obj in query])
#     return HttpResponse(content)


def load_content_publications(request):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Artwork.objects.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + LIMIT]
    content = ''.join([obj.as_html() for obj in query])
    hide_btn = query.count() < LIMIT
    return JsonResponse(content = content, hide_btn = hide_btn)


def load_content_tag(request, pk):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Tag.objects.get(pk = pk).publications.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    hide_btn = query.count() < LIMIT
    return JsonResponse(content = content, hide_btn = hide_btn)


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
        hide_btn = query.count() < LIMIT
        return JsonResponse(content = content, hide_btn = hide_btn)

    else:
        return HttpResponse('Произошла ошибка')


def load_content_main(request):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Publication.objects.exclude(datetime__gte = from_date).annotate(likes_count=Count('likes')).order_by('-likes_count')[shown:shown + LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    hide_btn = query.count() < LIMIT
    return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_artist(request, pk):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    profile = get_object_or_404(ArtistProfile, pk = pk)
    query = profile.publication_set.all().order_by('-datetime')[shown:shown + LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    hide_btn = query.count() < LIMIT
    return JsonResponse(content = content, hide_btn = hide_btn)

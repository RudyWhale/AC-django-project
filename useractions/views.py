from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.template.loader import render_to_string
from datetime import datetime
from main.models import Publication, Artwork, Tag, ArtistProfile, Comment
from ArtChart.settings import CONTENT_ITEMS_LIMIT, ARTIST_PROFILES_LIMIT
import json


def like(request):
	user = request.user;

	if user.is_authenticated:
		publ_pk = None;
		if request.method == 'GET':
			publ_pk = int(request.GET['publication_pk'])

		likes = 0;

		if publ_pk:
			publ = Publication.objects.get(pk = publ_pk)

			if user not in publ.likes.all():
				publ.likes.add(user)
			else:
				publ.likes.remove(user)
			likes = publ.likes.count();

		return HttpResponse(likes)

	else:
		return HttpResponse(status=401)


def subscribe(request):
	user = request.user;

	if user.is_authenticated:
		profile_pk = None;
		if request.method == 'GET':
			profile_pk = int(request.GET['profile_pk'])

		subs = 0;

		if profile_pk:
			profile = ArtistProfile.objects.get(pk = profile_pk)

			if profile.user == user:
				return JsonResponse({'count': subs, 'error_msg': 'Вы не можете подписаться на собственный аккаунт'})
			if user not in profile.subscribers.all():
				profile.subscribers.add(user)
			else:
				profile.subscribers.remove(user)
			subs = profile.subscribers.count();

		return JsonResponse({'count': subs, 'error_msg': ''})

	else:
		return JsonResponse({'count': 0, 'error_msg': 'Войдите на сайт, чтобы следить за деятельностью любимых авторов'})


def comment(request):
	user = request.user;

	if user.is_authenticated:
		publ_pk = None
		text = None
		if request.method == 'GET':
			publ_pk = int(request.GET['publication_pk'])
			text = request.GET['text']

		if publ_pk:
			publication = Publication.objects.get(pk = publ_pk)
			comment = Comment.objects.create(
				publication = publication,
				author = user,
				date = datetime.now(),
				text = text
			)

		result = render_to_string('main/includes/artwork comment.html', {'comment': comment, 'user': user})
		return HttpResponse(result)

	else:
		return HttpResponse(status=401)


def load_content_publications(request):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Artwork.objects.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
    content = ''.join([obj.as_html() for obj in query])
    hide_btn = query.count() < CONTENT_ITEMS_LIMIT
    return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_tag(request, pk):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Tag.objects.get(pk = pk).publications.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    hide_btn = query.count() < CONTENT_ITEMS_LIMIT
    return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_feed(request):
    user = request.user
    if user.is_authenticated:
        from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
        publications = Publication.objects.exclude(datetime__gt = from_date).filter(author__in = user.subscriptions.all()).order_by('-datetime')
        shown = int(request.GET['shown'])
        query = publications.order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
        content = ''.join([obj.artwork.as_html() for obj in query])
        hide_btn = query.count() < CONTENT_ITEMS_LIMIT
        return JsonResponse({'content': content, 'hide_btn': hide_btn})

    else:
        return HttpResponse('Произошла ошибка')


def load_content_main(request):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    query = Publication.objects.exclude(datetime__gte = from_date).annotate(likes_count=Count('likes')).order_by('-likes_count')[shown:shown + CONTENT_ITEMS_LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    hide_btn = query.count() < CONTENT_ITEMS_LIMIT
    return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_artist(request, pk):
    from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
    shown = int(request.GET['shown'])
    profile = get_object_or_404(ArtistProfile, pk = pk)
    query = profile.publication_set.all().order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
    content = ''.join([obj.artwork.as_html() for obj in query])
    hide_btn = query.count() < CONTENT_ITEMS_LIMIT
    return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_artist_profiles(request):
	# from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	query = ArtistProfile.objects.annotate(subs_count=Count('subscribers')).order_by('-subs_count')[shown:shown + ARTIST_PROFILES_LIMIT]
	content = ''.join([obj.as_html(request.user) for obj in query])
	hide_btn = query.count() < ARTIST_PROFILES_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def delete_comment(request, pk):
	initiator = request.user

	if request.user.is_authenticated:
		comment = get_object_or_404(Comment, pk = pk)

		if comment.author == initiator:
			comment.delete()
			return HttpResponse('')

		else: return HttpResponse(status=401)

	else: return HttpResponse(status=401)


def delete_publication(request, pk):
	initiator = request.user

	if request.user.is_authenticated:
		publication = get_object_or_404(Publication, pk = pk)
		profile = publication.author

		if profile.user == initiator:
			publication.delete()
			return redirect('artist', pk=profile.pk)

		else:
			args = {
				'msg_header': 'Произошла ошибка',
				'msg_text':  'Возможно, вы пытаетесь удалить чужую публикацию',
				'from_page': request.META.get('HTTP_REFERER')
			}
			return render(request, 'main/info message.html', args)

	else:
		args = {
			'msg_header': 'Произошла ошибка',
			'msg_text':  'В данный момент вы не авторизованы. Если вы пытаетесь удалить вашу публикацию, войдите на сайт',
			'from_page': request.META.get('HTTP_REFERER')
		}
		return render(request, 'main/info message.html', args)

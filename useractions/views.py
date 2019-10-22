from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.template.loader import render_to_string
from datetime import datetime
from main.models import Publication, Artwork, Tag, ArtistProfile, Comment
from ArtChart.settings import CONTENT_ITEMS_LIMIT, ARTIST_PROFILES_LIMIT, COMMENT_MAX_LENGTH
import json


def like(request):
	user = request.user;

	if user.is_authenticated:
		if 'publication_pk' not in request.GET: return HttpResponse(status=400)

		publ_pk = int(request.GET['publication_pk'])
		likes = 0;
		publ = Publication.objects.get(pk = publ_pk)

		if user not in publ.likes.all():
			publ.likes.add(user)
			label = "не нравится"
		else:
			publ.likes.remove(user)
			label = "нравится"

		likes = publ.likes.count();
		return JsonResponse({'count': likes, 'btn_text': label})

	else: return HttpResponse(status=401)


def subscribe(request):
	user = request.user;

	if user.is_authenticated:
		if 'profile_pk' not in request.GET: return HttpResponse(status=400)

		profile_pk = int(request.GET['profile_pk'])
		subs = 0;
		profile = ArtistProfile.objects.get(pk = profile_pk)

		if profile.user == user:
			return HttpResponse(status=403)
		if user not in profile.subscribers.all():
			profile.subscribers.add(user)
		else:
			profile.subscribers.remove(user)

		subs = profile.subscribers.count();

		return HttpResponse(subs)

	else: return HttpResponse(status=401)


def comment(request):
	user = request.user;

	if user.is_authenticated:
		if not all(key in request.GET for key in ['publication_pk', 'text']):
			return HttpResponse(status=400)

		publ_pk = int(request.GET['publication_pk'])
		text = request.GET['text'].strip().replace('  ', ' ')

		if not text or len(text) > COMMENT_MAX_LENGTH: return HttpResponse(status=400)

		publication = Publication.objects.get(pk = publ_pk)
		comment = Comment.objects.create(
			publication = publication,
			author = user,
			datetime = datetime.now(),
			text = text
		)
		result = render_to_string('main/includes/artwork comment.html', {'comment': comment, 'user': user})
		return HttpResponse(result)

	else:
		return HttpResponse(status=401)


def load_content_publications(request):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	query = Artwork.objects.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.as_html() for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_tag(request, pk):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	query = Tag.objects.get(pk = pk).publications.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.artwork.as_html() for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_feed(request):
	user = request.user
	if user.is_authenticated:
		if not all(key in request.GET for key in ['from_tstamp', 'shown']):
			return HttpResponse(status=400)

		from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
		shown = int(request.GET['shown'])
		publications = Publication.objects.exclude(datetime__gt = from_date).filter(author__in = user.subscriptions.all()).order_by('-datetime')
		query = publications.order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
		content = ''.join([obj.artwork.as_html() for obj in query])
		hide_btn = query.count() < CONTENT_ITEMS_LIMIT
		return JsonResponse({'content': content, 'hide_btn': hide_btn})

	else:
		return HttpResponse(status=400)


def load_content_main(request):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	query = Publication.objects.exclude(datetime__gte = from_date).annotate(likes_count=Count('likes')).order_by('-likes_count')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.artwork.as_html() for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_artist(request, pk):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	profile = get_object_or_404(ArtistProfile, pk = pk)
	query = profile.publication_set.all().order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.artwork.as_html() for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_artist_profiles(request):
	if not 'shown' in request.GET: return HttpResponse(status=400)

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

		else: return HttpResponse(status=403)

	else: return HttpResponse(status=401)


def delete_publication(request, pk):
	initiator = request.user

	if request.user.is_authenticated:
		publication = get_object_or_404(Publication, pk = pk)
		profile = publication.author

		if profile.user == initiator:
			publication.delete()
			return redirect('artist', pk=profile.pk)

		else: return HttpResponse(status=403)

	else: return HttpResponse(status=401)

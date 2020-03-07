from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.template.loader import render_to_string
from django.contrib.auth import logout as user_logout
from django.urls import reverse
from datetime import datetime
from main.models import Publication, Artwork, Tag, ArtistProfile, Comment, Reply, ArtworkCategory
from ArtChart.settings import CONTENT_ITEMS_LIMIT, ARTIST_PROFILES_LIMIT, COMMENT_MAX_LENGTH
import json


def like(request):
	user = request.user;

	if user.is_authenticated:
		if 'publication_pk' not in request.GET: return HttpResponse(status=400)

		likes = 0;
		publication = get_object_or_404(Publication, pk=int(request.GET['publication_pk']))

		if user not in publication.likes.all():
			publication.likes.add(user)
			label = 'не нравится'
		else:
			publication.likes.remove(user)
			label = 'нравится'

		likes = publication.likes.count();
		return JsonResponse({'count': likes, 'label': label})

	else: return HttpResponse(status=401)


def subscribe(request):
	user = request.user;

	if user.is_authenticated:
		if 'profile_pk' not in request.GET: return HttpResponse(status=400)

		profile = get_object_or_404(ArtistProfile, pk=int(request.GET['profile_pk']))
		subs = 0;

		if profile.user == user:
			return HttpResponse(status=403)

		if user not in profile.subscribers.all():
			profile.subscribers.add(user)
			label = 'отписаться'
		else:
			profile.subscribers.remove(user)
			label = 'подписаться'

		subs = profile.subscribers.count();

		return JsonResponse({'count': subs, 'label': label})

	else: return HttpResponse(status=401)


def comment(request):
	user = request.user;

	if user.is_authenticated:
		if not all(key in request.GET for key in ['publication_pk', 'text']):
			return HttpResponse(status=400)

		text = request.GET['text'].strip().replace('  ', ' ')
		if not text or len(text) > COMMENT_MAX_LENGTH: return HttpResponse(status=400)

		publication = get_object_or_404(Publication, pk=int(request.GET['publication_pk']))

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


def reply(request):
	user = request.user;

	if user.is_authenticated:
		if not all(key in request.GET for key in ['comment_pk', 'text']):
			return HttpResponse(status=400)

		text = request.GET['text'].strip().replace('  ', ' ')
		if not text or len(text) > COMMENT_MAX_LENGTH: return HttpResponse(status=400)

		comment = get_object_or_404(Comment, pk=int(request.GET['comment_pk']))

		reply = Reply.objects.create(
			author = user,
			datetime = datetime.now(),
			text = text,
			comment = comment
		)
		result = render_to_string('main/includes/artwork comment reply.html', {'reply': reply, 'user': user})
		return HttpResponse(result)

	else:
		return HttpResponse(status=401)


def load_content_category(request, pk):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	category = get_object_or_404(ArtworkCategory, pk=pk)
	query = category.artwork_set.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.as_html(request) for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_tag(request, pk):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	tag = get_object_or_404(Tag, pk=pk)
	query = tag.publications.exclude(datetime__gt = from_date).order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.artwork.as_html(request) for obj in query])
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
		content = ''.join([obj.artwork.as_html(request) for obj in query])
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
	content = ''.join([obj.artwork.as_html(request) for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_content_artist(request, pk):
	if not all(key in request.GET for key in ['from_tstamp', 'shown']):
		return HttpResponse(status=400)

	from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	profile = get_object_or_404(ArtistProfile, pk = pk)
	query = profile.publication_set.all().order_by('-datetime')[shown:shown + CONTENT_ITEMS_LIMIT]
	content = ''.join([obj.artwork.as_html(request) for obj in query])
	hide_btn = query.count() < CONTENT_ITEMS_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


def load_artist_profiles(request):
	if not 'shown' in request.GET: return HttpResponse(status=400)

	# from_date = datetime.fromtimestamp(float(request.GET['from_tstamp']))
	shown = int(request.GET['shown'])
	query = ArtistProfile.objects.annotate(subs_count=Count('subscribers')).order_by('-subs_count')[shown:shown + ARTIST_PROFILES_LIMIT]
	content = ''.join([obj.as_html(request) for obj in query])
	hide_btn = query.count() < ARTIST_PROFILES_LIMIT
	return JsonResponse({'content': content, 'hide_btn': hide_btn})


'''
Deletes object from DB. User has to be authenticated and same with author
'''
def delete_object(request, object, author, redirect_to=''):
	initiator = request.user

	if request.user.is_authenticated:

		if author == initiator:
			object.delete()

			if redirect_to: return redirect(redirect_to)
			return HttpResponse('')

		else: return HttpResponse(status=403)

	else: return HttpResponse(status=401)


def delete_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	author = comment.author
	return delete_object(request, comment, author)


def delete_reply(request, pk):
	reply = get_object_or_404(Reply, pk=pk)
	author = reply.author
	return delete_object(request, reply, author)


def delete_publication(request, pk):
	publication = get_object_or_404(Publication, pk=pk)
	author = publication.author.user
	redirect = reverse('artist', args=[author.pk,])
	return delete_object(request, publication, author, redirect)


def clear_notifications(request):
	if not request.user.is_authenticated:
		return HttpResponse(status=401)

	request.user.webnotification_set.all().delete()
	return HttpResponse('')


def logout(request):
	user_logout(request)
	return HttpResponse('')

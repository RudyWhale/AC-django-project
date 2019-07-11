from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from main.models import Publication, ArtistProfile, Comment
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

		return JsonResponse({'count': likes, 'error_msg': ''})

	else:
		return JsonResponse({'count': 0, 'error_msg': 'Войдите на сайт, чтобы отмечать понравившиеся записи'})


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
			Comment.objects.create(
				publication = publication,
				author = user,
				date = datetime.now(),
				text = text
			)

		return HttpResponse("")

	else:
		return HttpResponse("Войдите на сайт, чтобы комментировать публикации")

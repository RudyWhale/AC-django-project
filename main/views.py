from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Publication, Artwork, Article, ArtistProfile, Tag

def index(request):
	publications = Publication.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')
	return render(request, 'main/index.html', {	'publications': publications,
												'content_header': 'Популярно:'})


def artist(request, pk):
	profile = get_object_or_404(ArtistProfile, pk = pk)
	user = profile.user;
	publications = profile.publication_set.all().order_by('-date')
	create_publication = True if profile.user == request.user else False
	return render(request, 'main/artist.html', {'user': user,
												'profile': profile,
												'publications': publications,
												'create_publication': create_publication})


def artists(request):
	artists = ArtistProfile.objects.all()
	return render(request, 'main/artists.html', {'artists': artists})


def artworks(request):
	publications = Artwork.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')
	return render(request, 'main/publications.html', {'publications': publications, 'content_header': 'популярные работы'})


def articles(request):
	publications = Article.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')
	return render(request, 'main/publications.html', {'publications': publications, 'content_header': 'популярные статьи'})


def artwork(request, pk):
	artwork = get_object_or_404(Artwork, pk = pk)
	related_pubs = Artwork.objects.exclude(pk = pk)[:4]
	return render(request, 'main/artwork.html', {'artwork': artwork, 'related_pubs': related_pubs})


def article(request, pk):
	article = get_object_or_404(Article, pk = pk)
	return render(request, 'main/article.html', {'article': article, 'author': article.author})


def feed(request):
	if request.user.is_authenticated:
		publications = Publication.objects.none()
		for artistprofile in request.user.subscriptions.all():
			publications = publications.union(artistprofile.publication_set.all())

		publications.order_by('-date')
		return render(request, 'main/publications.html', {'publications': publications, 'content_header': 'ваша лента:'})

	else:
		args = {
			'msg_header': "Этот раздел досутен только авторизованным пользователям",
			'msg_text':  "Войдите на сайт для того, чтобы подписываться на блоги художников и видеть вашу персональную ленту",
			'from_page': request.META.get('HTTP_REFERER')
		}
		return render(request, 'main/info message.html', args)


def become_artist(request):
	if request.user.is_authenticated:
		if  request.user.has_perm('main.add_artistprofile'):
			return redirect('register_as_artist')
		else:
			args = {
				'msg_header': 'Вы не можете сейчас стать художником',
				'msg_text':  'На данный момент вы не можете создать аккаунт художника. Если хотите сотрудничать, свяжитесь с нами',
				'from_page': request.META.get('HTTP_REFERER')
			}
			return render(request, 'main/info message.html', args)

	else:
		args = {
			'msg_header': 'Войдите на сайт',
			'msg_text':  'Вы приходите к нам и говорите, что хотите стать автором, но вы даже не называете своего имени. Авторизуйтесь, чтобы выполнить это действие с уважением',
			'from_page': request.META.get('HTTP_REFERER')
		}
		return render(request, 'main/info message.html', args)


def tag(request, pk):
	tag = get_object_or_404(Tag, pk = pk)
	publications = tag.publications.all()
	args = {'publications': publications, 'content_header': 'Поиск по тегу ' + tag.name + ':'}
	return render(request, 'main/publications.html', args)

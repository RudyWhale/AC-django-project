from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse
from django.core.mail import send_mail
from datetime import datetime
from .models import Publication, Artwork, ArtistProfile, Tag
from ArtChart.settings import CONTENT_ITEMS_LIMIT, ARTIST_PROFILES_LIMIT, COMMENT_MAX_LENGTH, ADMIN_EMAIL_ADRESS, EMAIL_HOST_USER

def index(request):
	publications = Publication.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = datetime.now().timestamp()
	args = {
		'meta_title': 'ArtChart',
		'meta_description': 'ArtChart - портал для художников, дизайнеров и людей, интересующихся искусством и творчеством. ' \
							'Здесь художники рассказывают о своих работах. Зарегистрировавшись, вы сможете отмечать понравившиеся работы, ' \
							'подписываться на любимых авторов и следить за их деятельностью на портале',
		'publications': publications,
		'content_header': 'популярно:',
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load content main')
	}
	return render(request, 'main/publications.html', args)


def artist(request, pk):
	profile = get_object_or_404(ArtistProfile, pk = pk)
	publications = profile.publication_set.all().order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = datetime.now().timestamp()
	user = profile.user
	create_publication = True if profile.user == request.user else False
	args = {
		'meta_title': f'{user.username}',
		'meta_description': f'Блог пользователя {user.username} на ArtChart. {profile.desc}',
		'user': user,
		'profile': profile,
		'content_header': 'Блог автора:',
		'publications': publications,
		'create_publication': create_publication,
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load content artist', args=(profile.pk,))
	}
	return render(request, 'main/publications.html', args)


def artists(request):
	artists = ArtistProfile.objects.all().annotate(subs_count=Count('subscribers')).order_by('-subs_count')[:ARTIST_PROFILES_LIMIT]
	infinite = artists.count() == ARTIST_PROFILES_LIMIT
	timestamp = datetime.now().timestamp()
	args = {
		'meta_title': 'Блоги на ArtChart',
		'meta_description': 'Посмотреть блоги художников, зарегистрированных на ArtChart',
		'artists': artists,
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load artist profiles')
	}
	return render(request, 'main/artists.html', args)


def artworks(request):
	publications = Artwork.objects.order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = datetime.now().timestamp()
	args = {
		'meta_title': 'Работы на ArtChart',
		'meta_description': 'Посмотреть работы художников, зарегистрированных на ArtChart',
		'publications': publications,
		'content_header': 'картины',
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load content publications')
	}
	return render(request, 'main/publications.html', args)


def artwork(request, pk):
	artwork = get_object_or_404(Artwork, pk = pk)
	author = artwork.author.user
	related_pubs = Artwork.objects.exclude(pk = pk)[:4]
	show_delete_link = request.user == author
	args = {
		'meta_title': f'{artwork.name}',
		'meta_description': f'Работа художника {author.username} "{artwork.name}". {artwork.desc}',
		'artwork': artwork,
		'related_pubs': related_pubs,
		'delete_link': show_delete_link,
		'max_comment_length': COMMENT_MAX_LENGTH
	}
	return render(request, 'main/artwork.html', args)


def feed(request):
	user = request.user

	if user.is_authenticated:
		publications = Publication.objects.filter(author__in = user.subscriptions.all()).order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
		infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
		timestamp = datetime.now().timestamp()
		args = {
			'meta_title': 'Лента',
			'meta_description': '',
			'publications': publications,
			'content_header': 'ваша лента:',
			'infinite': infinite,
			'timestamp': timestamp,
			'load_content_url': reverse('load content feed')
		}
		return render(request, 'main/publications.html', args)

	else:
		args = {
			'meta_title': 'Карамба!',
			'meta_description': '',
			'msg_header': "Этот раздел досутен только авторизованным пользователям",
			'msg_text':  "Войдите на сайт для того, чтобы подписываться на блоги художников и видеть вашу персональную ленту",
			'from_page': request.META.get('HTTP_REFERER')
		}
		return render(request, 'main/info message.html', args)


def become_artist(request):
	if request.user.is_authenticated:
		if  request.user.has_perm('main.add_artistprofile'):
			return redirect('register as artist')
		else:
			args = {
				'meta_title': 'Карамба!',
				'meta_description': '',
				'msg_header': 'У вас нет приглашения',
				'msg_text': 'К сожалению, в текущий момент мы не принимаем в наши ряды случайных прохожих. ' \
							'Для того, чтобы создать профиль художника, вам необходимо получить приглашение от администрации',
				'from_page': request.META.get('HTTP_REFERER')
			}
			return render(request, 'main/info message.html', args)

	else:
		args = {
			'meta_title': 'Карамба!',
			'meta_description': '',
			'msg_header': 'Войдите на сайт',
			'msg_text':  'Простите, но мы хотим знать, с кем имеем дело. Пожалуйста, авторизуйтесь, если хотите создать аккаунт художника на ArtChart',
			'from_page': request.META.get('HTTP_REFERER')
		}
		return render(request, 'main/info message.html', args)


def tag(request, pk):
	tag = get_object_or_404(Tag, pk = pk)
	publications = tag.publications.order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = datetime.now().timestamp()
	args = {
		'meta_title': f'Тег {tag.name}',
		'meta_description': f'Поиск публикаций по тегу {tag.name} на ArtChart',
		'publications': publications,
		'content_header': 'Поиск по тегу ' + tag.name + ':',
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load content tag', args=(tag.pk,))
	}
	return render(request, 'main/publications.html', args)


def feedback(request):
	if request.method == 'POST':
		message = request.POST['message']
		theme = 'ArtChart: сообщение от пользователя'

		if request.user.is_authenticated:
			theme += ' ' + request.user.username

		send_mail(
			theme,
			message,
			EMAIL_HOST_USER,
			[ADMIN_EMAIL_ADRESS,]
		)

		args = {
			'meta_title': 'Спасибо!',
			'meta_description': '',
			'msg_header': "Ваше сообщение было отправлено",
			'msg_text':  "Спасибо за обратную связь! Нам важно ваше мнение о проекте, ведь вы можете помочь сделать его лучше",
		}
		return render(request, 'main/info message.html', args)

	else:
		args = {
			'meta_title': 'Напишите нам',
			'meta_description': '',
		}
		return render(request, 'main/feedback.html', args)


def robots(request):
	return render(request, 'robots.txt', content_type="text/plain")

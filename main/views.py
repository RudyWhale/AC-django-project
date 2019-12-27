from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
from .models import Publication, Artwork, ArtistProfile, Tag, UserSettings, ProfileSettings
from .forms import *
from ArtChart.settings import *

def index(request):
	publications = Publication.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = timezone.now().timestamp()
	args = {
		'meta_title': 'ArtChart',
		'meta_description': 'ArtChart - портал для художников, дизайнеров и людей, интересующихся искусством и творчеством. ' \
							'Здесь художники рассказывают о своих работах. Зарегистрировавшись, вы сможете отмечать понравившиеся работы, ' \
							'подписываться на любимых авторов и следить за их деятельностью на портале',
		'site_description': True,
		'page': 'index',
		'publications': publications,
		'content_header': 'популярные работы',
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load content main'),
	}
	return render(request, 'main/publications.html', args)


def artist(request, pk):
	user = get_object_or_404(User, pk=pk)
	profile = ArtistProfile.objects.get_or_create(user=user)[0]
	publications = profile.publication_set.all().order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = timezone.now().timestamp()
	create_publication = True if profile.user == request.user else False
	args = {
		'meta_title': f'{user.username}',
		'meta_description': f'Блог пользователя {user.username} на ArtChart. {profile.desc}',
		'page': 'artist',
		'user': user,
		'profile': profile,
		'content_header': 'работы автора',
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
	timestamp = timezone.now().timestamp()
	args = {
		'meta_title': 'Блоги на ArtChart',
		'meta_description': 'Посмотреть блоги художников, зарегистрированных на ArtChart',
		'page': 'artists',
		'artists': artists,
		'infinite': infinite,
		'timestamp': timestamp,
		'load_content_url': reverse('load artist profiles')
	}
	return render(request, 'main/artists.html', args)


def artworks(request):
	publications = Artwork.objects.order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = timezone.now().timestamp()
	args = {
		'meta_title': 'Работы на ArtChart',
		'meta_description': 'Посмотреть работы художников, зарегистрированных на ArtChart',
		'page': 'artworks',
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
	related_pubs = Artwork.objects.exclude(pk = pk)[:3]
	show_delete_link = request.user == author
	args = {
		'meta_title': f'{artwork.name}',
		'meta_description': f'Работа художника {author.username} "{artwork.name}". {artwork.desc}',
		'page': 'artwork',
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
		timestamp = timezone.now().timestamp()
		args = {
			'meta_title': 'Лента',
			'meta_description': '',
			'page': 'feed',
			'publications': publications,
			'content_header': 'ваша лента',
			'infinite': infinite,
			'timestamp': timestamp,
			'load_content_url': reverse('load content feed')
		}
		return render(request, 'main/publications.html', args)

	else:
		args = {
			'meta_title': 'Карамба!',
			'meta_description': '',
			'page': 'feed',
			'msg_header': "Этот раздел досутен только авторизованным пользователям",
			'msg_text':  "Войдите на сайт для того, чтобы подписываться на блоги художников и видеть вашу персональную ленту",
			'links': {
				'На страницу входа': reverse('login'),
				'На главную': reverse('index'),
			},
			'from_page': request.META.get('HTTP_REFERER')
		}
		return render(request, 'main/info message.html', args)


def tag(request, pk):
	tag = get_object_or_404(Tag, pk = pk)
	publications = tag.publications.order_by('-datetime')[:CONTENT_ITEMS_LIMIT - 1]
	infinite = publications.count() == (CONTENT_ITEMS_LIMIT - 1)
	timestamp = timezone.now().timestamp()
	args = {
		'meta_title': f'Тег {tag.name}',
		'meta_description': f'Поиск публикаций по тегу {tag.name} на ArtChart',
		'page': 'tag',
		'publications': publications,
		'content_header': f'публикации с тегом "{tag.name}"',
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
			'page': 'feedback',
			'msg_header': "Ваше сообщение было отправлено",
			'msg_text':  "Спасибо за обратную связь! Нам важно ваше мнение о проекте, ведь вы можете помочь сделать его лучше"
		}
		return render(request, 'main/info message.html', args)

	else:
		args = {
			'meta_title': 'Напишите нам',
			'meta_description': '',
			'page': 'feedback',
			'forms': {
				'Обратная связь': FeedbackForm(),
			},
			'submit_text': 'Отправить сообшение'
		}
		return render(request, 'main/form.html', args)


def robots(request):
	return render(request, 'robots.txt', content_type="text/plain")


def new_artwork(request):
	user = request.user

	try:
		profile = user.profile

	except AttributeError as e:
		args = {
			'meta_title': '',
			'meta_description': '',
			'page': 'new artwork',
			'msg_header': "Что-то пошло не так",
			'msg_text':  'Во время создания публикации нам не удалось найти ваш профиль художника. ' \
			'Вы можете написать нам об ошибке, и мы постараемся найти причину ее появления',
			'links': {
				'На главную': reverse('index'),
				'Напишите нам': reverse('feedback'),
			}
		}
		return SimpleTemplateResponse(template='main/info message.html', context=args, status=403)

	if request.method == 'POST':
		form = ArtworkCreationForm(request.POST, request.FILES)

		if form.is_valid():
			form.save(profile = profile)
			return redirect('artist', pk = profile.pk)

		else:
			args = {
				'meta_title': '',
				'meta_description': '',
				'page': 'new artwork',
				'msg_header': "Что-то пошло не так",
				'msg_text':  'Во время создания публикации произошла неизвестная ошибка. ' \
				'Если она повторяется, можете написать нам, и мы постараемся найти причину ее появления',
				'links': {
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='main/info message.html', context=args, status=400)

	else:
		args = {
			'page': 'new artwork',
			'forms': {
				'Новая работа': ArtworkCreationForm()
			},
			'submit_text': 'Создать работу',
		}
		return render(request, 'main/form.html', args)


def settings(request):
	user = request.user

	if not user.is_authenticated:
		args = {
			'meta_title': '',
			'meta_description': '',
			'page': 'settings',
			'msg_header': "Представьтесь, пожалуйста",
			'msg_text':  "Авторизуйтесь для доступа к странице настроек",
			'links': {
				'На страницу входа': reverse('login'),
				'На главную': reverse('index'),
			}
		}
		return SimpleTemplateResponse(template='main/info message.html', context=args, status=400)

	settings = UserSettings.objects.get_or_create(user=user)[0]

	if request.method == 'POST':
		settings_form = UserSettingsForm(request.POST, instance=settings)
		profile_form = ArtistProfileForm(request.POST, request.FILES, instance=user.profile)

		if settings_form.is_valid(): settings_form.save()
		if profile_form.is_valid(): profile_form.save()

		args = {
			'meta_title': 'Настройки изменены',
			'meta_description': '',
			'page': 'settings',
			'msg_header': "Настройки были изменены",
			'msg_text':  "Мы сохранили изменения вашего профиля",
			'links': {
				'Ваша страница': reverse('artist', args=[request.user.pk,]),
				'На главную': reverse('index'),
			}
		}
		return render(request, 'main/info message.html', args)

	else:
		args = {
			'page': 'settings',
			'forms': {
				'Профиль': ArtistProfileForm(instance=user.profile),
				'Email-уведомления': UserSettingsForm(instance=user.usersettings)
			},
			'submit_text': 'Сохранить настройки'
		}
		return render(request, 'main/form.html', args)

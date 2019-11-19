from django.shortcuts import render, redirect
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.response import SimpleTemplateResponse
from main.models import ArtistProfile
from ArtChart.settings import EMAIL_HOST_USER, PROFILE_DESC_MAX_LENGTH, PROFILE_AVATAR_MAX_SIZE, HOST
from .forms import ArtistCreationForm, RegistrationForm, ACPasswordResetForm, ACSetPasswordForm
from .snippets import get_hash


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			user = form.save()
			link = HOST + reverse('activate', args=[user.pk, get_hash(user)])
			message = f'Для завершения регистрации на портале ArtChart перейдите по ссылке: {link}.' \
						'\nЕсли вы получили это сообщение по ошибке, проигнорируйте его.'
			html = render_to_string('login/email_templates/end_registration.html', {'link': link})

			send_mail(
				'Завершите регистрацию на ArtChart',
				message,
				EMAIL_HOST_USER,
				[user.email],
				html_message = html,
			)

			args = {
				'header': 'Регистрация на сайте',
				'message': 'Мы отправили на указанную вами почту дальнейшие инструкции',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index')
				}
			}
			return render(request, 'login/message.html', args)

		else:
			args = {
				'header': 'Регистрация на сайте',
				'message':  "К сожалению, во время регистрации произошла ошибка. Если она повторяется, вы можете написать администрации",
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

	else:
		form = RegistrationForm()
		return render(request, 'login/register.html', {'form': form})


def logout(request):
	user_logout(request)
	return redirect('index')


def register_as_artist(request):
	if request.method == 'POST':
		form = ArtistCreationForm(request.POST, request.FILES)

		if form.is_valid():
			# Takes care of user permissions
			reg_perm = Permission.objects.get(name="Can add artist profile")
			download_perm = Permission.objects.get(name="Can add publication")
			request.user.user_permissions.remove(reg_perm)
			request.user.user_permissions.add(download_perm)

			# Creates new artist profile
			profile = form.save(request.user)
			args = {
				'header': 'Создание профиля',
				'message': 'Профиль художника был успешно создан. Теперь вы можете создавать публикации, которые будут видны другим пользователям',
				'links': {
					'Ваша страница': reverse('artist', args=[profile.pk,]),
					'На главную': reverse('index'),
				},
			}
			return render(request, 'login/message.html', args)

		else:
			args = {
				'header': 'Создание профиля',
				'message':  'К сожалению, во время регистрации произошла ошибка. Если она повторяется, вы можете написать администрации',
				'links': {
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

	else:
		if (request.user.has_perm('main.add_artistprofile')):
			args = {
				'form': ArtistCreationForm(),
				'max_desc_length': PROFILE_DESC_MAX_LENGTH
			}
			return render(request, 'login/register as artist.html', args)

		else: return redirect('become artist')


def activate(request, pk, hash):
	try:
		user = User.objects.get(pk = pk)

		if (get_hash(user) == hash):
			user.is_active = True
			user.save()
			args = {
				'header': 'Регистрация на сайте',
				'message':  'Ваш аккаунт успешно активирован. Добро пожаловать на ArtChart! :)',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
				}
			}
			return render(request, 'login/message.html', args)

		else:
			args = {
				'header': 'Регистрация на сайте',
				'message':  'К сожалению, этот хэш недействителен. Возможно, вы уже активировали свой аккаунт. ' \
							'Если ошибка повторяется, вы можете написать администрации',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

	except User.DoesNotExist:
		args = {
			'header': 'Регистрация на сайте',
			'message':  'К сожалению, эта ссылка недействительна. Если ошибка повторяется, вы можете написать администрации',
			'links': {
				'Войти на сайт': reverse('login'),
				'На главную': reverse('index'),
				'Напишите нам': reverse('feedback'),
			}
		}
		return SimpleTemplateResponse(template='login/message.html', context=args, status=400)


def password_reset(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		try:
			user = User.objects.get(email = email)
			link = HOST + reverse('password change', args=[user.pk, get_hash(user)])
			html = render_to_string('login/email_templates/password_reset.html', {'link': link})

			send_mail(
				'Смена пароля на ArtChart',
				f'Для смены пароля на ArtChart перейдите по ссылке: {link}\n' \
				'Если вы получили это сообщение по ошибке, просто проигнорируйте его',
				EMAIL_HOST_USER,
				[email],
				html_message = html,
			)

			args = {
				'header': 'Восстановление пароля',
				'message':  'Проверьте электронную почту! Мы отправили вам инструкции по смене пароля. ' \
							'Если письма нет, возможно, оно попало в спам',
				'links': {
					'На главную': reverse('index'),
				}
			}
			return render(request, 'login/message.html', args)

		except User.DoesNotExist:
			args = {
				'header': 'Восстановление пароля',
				'message':  'К сожалению, эта ссылка недействительна. Если ошибка повторяется, вы можете написать администрации',
				'links': {
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

	else:
		form = ACPasswordResetForm()
		return render(request, 'login/password reset.html', {'form': form})


def password_change(request, pk, hash):
	try:
		user = User.objects.get(pk = pk)

		if get_hash(user) != hash:
			args = {
				'header': 'Восстановление пароля',
				'message':  'К сожалению, эта ссылка недействительна. Возможно, вы уже восстановили свой пароль. ' \
							'Если ошибка повторяется, вы можете написать администрации',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

		if request.method == 'POST':
			form = ACSetPasswordForm(user, request.POST)

			if form.is_valid():
				form.save()
				args = {
					'header': 'Восстановление пароля',
					'message':  'Пароль был успешно изменен!',
					'links': {
						'Войти на сайт': reverse('login'),
						'На главную': reverse('index'),
						'Напишите нам': reverse('feedback'),
					}
				}
				return render(request, 'login/message.html', args)

			else:
				args = {
					'header': 'Восстановление пароля',
					'message':  "Во время изменения пароля произошла ошибка. Если она повторяется, вы можете написать администрации",
					'links': {
						'На главную': reverse('index'),
						'Напишите нам': reverse('feedback'),
					}
				}
				return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

		else:
			form = ACSetPasswordForm(user)
			return render(request, 'login/password change.html', {'form': form, 'hash': hash})

	except User.DoesNotExist:
		args = {
			'header': 'Восстановление пароля',
			'message':  'К сожалению, эта ссылка недействительна. Возможно, вы уже восстановили свой пароль. ' \
						'Если ошибка повторяется, вы можете написать администрации',
			'links': {
				'Войти на сайт': reverse('login'),
				'На главную': reverse('index'),
				'Напишите нам': reverse('feedback'),
			}
		}
		return SimpleTemplateResponse(template='login/message.html', context=args, status=400)

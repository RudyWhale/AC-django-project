from django.shortcuts import render, redirect
from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.response import SimpleTemplateResponse
from django.templatetags.static import static
from ArtChart.settings import EMAIL_HOST_USER, HOST
from .forms import ACAuthenticationForm, RegistrationForm, ACPasswordResetForm, ACSetPasswordForm
from .snippets import get_hash


def login(request):
	header = 'Вход на сайт'
	action = reverse('login')
	links =  {
		'Забыли пароль?': reverse('password reset'),
		'Регистрация': reverse('register'),
		'На главную': reverse('index'),
	}

	if request.method == 'POST':
		form = ACAuthenticationForm(request, data=request.POST)

		if form.is_valid():
			user_login(request, form.get_user())
			return redirect('index')

		args = {
			'header': header,
			'message': 'Ошибка :( Проверьте правильность ввода',
			'form': form,
			'action_url': action,
			'submit_text': 'Войти',
			'links': links,
		}
		return render(request, 'login/login.html', args)

	else:
		args = {
			'header': header,
			'form': ACAuthenticationForm(request),
			'action_url': action,
			'submit_text': 'Войти',
			'links': links,
		}
		return render(request, 'login/login.html', args)


def register(request):
	header = 'Регистрация на сайте'
	links =  {
		'Войти на сайт': reverse('login'),
		'На главную': reverse('index'),
	}

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
				'header': header,
				'message': 'Мы отправили на указанную вами почту дальнейшие инструкции',
				'links': links,
			}
			return render(request, 'login/login.html', args)

		else:
			links['Напишите нам'] = reverse('feedback')
			args = {
				'header': header,
				'message':  "К сожалению, во время регистрации произошла ошибка. Если она повторяется, вы можете написать администрации",
				'links': links,
			}
			return SimpleTemplateResponse(template='login/login.html', context=args, status=400)

	else:
		args = {
			'header': header,
			'form': RegistrationForm(),
			'scripts': [static('login/reg_form.js'),],
			'action_url': reverse('register'),
			'submit_text': 'Отправить',
			'links': links,
		}
		return render(request, 'login/login.html', args)


def activate(request, pk, hash):
	header = 'Регистрация на сайте'

	try:
		user = User.objects.get(pk = pk)

		if (get_hash(user) == hash):
			user.is_active = True
			user.save()

			# sends welcome email
			message = 'Рады сообщить, что только что мы активировали ваш аккаунт!'
			html = render_to_string('login/email_templates/welcome.html', {'username': user.username})
			send_mail(
				'Добро пожаловать!',
				message,
				EMAIL_HOST_USER,
				[user.email],
				html_message = html,
			)

			args = {
				'header': header,
				'message':  'Ваш аккаунт успешно активирован. Добро пожаловать на ArtChart! :)',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
				}
			}
			return render(request, 'login/login.html', args)

		else:
			args = {
				'header': header,
				'message':  'К сожалению, эта ссылка недействительна. Возможно, вы уже активировали свой аккаунт. ' \
							'Если ошибка повторяется, вы можете написать администрации',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/login.html', context=args, status=400)

	except User.DoesNotExist:
		args = {
			'header': header,
			'message':  'К сожалению, эта ссылка недействительна. Если ошибка повторяется, вы можете написать администрации',
			'links': {
				'Войти на сайт': reverse('login'),
				'На главную': reverse('index'),
				'Напишите нам': reverse('feedback'),
			}
		}
		return SimpleTemplateResponse(template='login/login.html', context=args, status=400)


def logout(request):
	user_logout(request)
	return redirect('index')


def password_reset(request):
	header = 'Восстановление пароля'

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
				'header': header,
				'message':  'Проверьте электронную почту! Мы отправили вам инструкции по смене пароля. ' \
							'Если письма нет, возможно, оно попало в спам',
				'links': {'На главную': reverse('index'),}
			}
			return render(request, 'login/login.html', args)

		except User.DoesNotExist:
			args = {
				'header': header,
				'message':  'К сожалению, эта ссылка недействительна. Если ошибка повторяется, вы можете написать администрации',
				'links': {
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/login.html', context=args, status=400)

	else:
		args = {
			'header': header,
			'form': ACPasswordResetForm(),
			'action_url': reverse('password reset'),
			'submit_text': 'Сбросить пароль',
			'links': {
				'На главную': reverse('index'),
			}
		}
		return render(request, 'login/login.html', args)


def password_change(request, pk, hash):
	header = 'Восстановление пароля'

	try:
		user = User.objects.get(pk = pk)

		if get_hash(user) != hash:
			args = {
				'header': header,
				'message':  'К сожалению, эта ссылка недействительна. Возможно, вы уже восстановили свой пароль. ' \
							'Если ошибка повторяется, вы можете написать администрации',
				'links': {
					'Войти на сайт': reverse('login'),
					'На главную': reverse('index'),
					'Напишите нам': reverse('feedback'),
				}
			}
			return SimpleTemplateResponse(template='login/login.html', context=args, status=400)

		if request.method == 'POST':
			form = ACSetPasswordForm(user, request.POST)

			if form.is_valid():
				form.save()
				args = {
					'header': header,
					'message':  'Пароль был успешно изменен! Теперь можете войти на сайт со своим новым паролем',
					'links': {
						'Войти на сайт': reverse('login'),
						'На главную': reverse('index'),
						'Напишите нам': reverse('feedback'),
					}
				}
				return render(request, 'login/login.html', args)

			else:
				args = {
					'header': header,
					'message':  "Во время изменения пароля произошла ошибка. Если она повторяется, вы можете написать администрации",
					'links': {
						'На главную': reverse('index'),
						'Напишите нам': reverse('feedback'),
					}
				}
				return SimpleTemplateResponse(template='login/login.html', context=args, status=400)

		else:
			args = {
				'scripts': [static('login/reg_form.js'),],
				'header': header,
				'form': ACSetPasswordForm(user),
				'action_url': reverse('password change', args=[user.pk, hash]),
				'submit_text': 'Сменить пароль',
			}
			return render(request, 'login/login.html', args)

	except User.DoesNotExist:
		args = {
			'header': header,
			'message':  'К сожалению, эта ссылка недействительна. Возможно, вы уже восстановили свой пароль. ' \
						'Если ошибка повторяется, вы можете написать администрации',
			'links': {
				'Войти на сайт': reverse('login'),
				'На главную': reverse('index'),
				'Напишите нам': reverse('feedback'),
			}
		}
		return SimpleTemplateResponse(template='login/login.html', context=args, status=400)

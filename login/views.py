from django.shortcuts import render, redirect
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse
from main.models import ArtistProfile
from ArtChart.settings import EMAIL_HOST_USER
from .forms import ArtistCreationForm, RegistrationForm, ACPasswordResetForm, ACSetPasswordForm
from .snippets import get_hash


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			user = form.save()

			message = ('Для завершения регистрации на портале ArtChart перейдите по ссылке:\n' +
						request.META['HTTP_HOST'] + reverse('activate', args=[user.pk, get_hash(user)]) +
						'\nЕсли вы получили это сообщение по ошибке, проигнорируйте его.')
			send_mail(
				'Завершите регистрацию на ArtChart',
				message,
				EMAIL_HOST_USER,
				[user.email]
			)

			message = 'Мы отправили на указанную вами почту дальнейшие инструкции'
			return render(request, 'login/message.html', {'message': message})

		else:
			message = 'Во время регистрации произошла ошибка. Проверьте правильность введенных данных '
			return render(request, 'login/message.html', {'message': message})

	else:
		form = RegistrationForm()
		return render(request, 'login/register.html', {'form': form})


def change_password(request):
	return render(request, 'login/change-password.html')


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
			form.save(request.user)
			message = 'Профиль художника был успешно создан. Теперь вы можете создавать публикации, которые будут видны другим пользователям'
			return render(request, 'login/message.html', {'message': message})

		else:
			message = 'Во время создания профиля художника произошла ошибка. Пожалуйста, свяжитесь с администрацией сайта'
			return render(request, 'login/message.html', {'message': message})

	else:
		if (request.user.has_perm('main.add_artistprofile')):
			form = ArtistCreationForm()
			return render(request, 'login/register as artist.html', {'form': form})
		else:
			return redirect('become artist')


def activate(request, pk, hash):
	message = 'Произошла ошибка'

	try:
		user = User.objects.get(pk = pk)

		if (get_hash(user) == hash):
			user.is_active = True
			user.save()
			message = 'Ваш аккаунт успешно активирован. Добро пожаловать на ArtChart'

	except User.DoesNotExist:
		pass

	return render(request, 'login/message.html', {'message': message})


def password_reset(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		try:
			user = User.objects.get(email = email)
			link = request.META['HTTP_HOST'] + reverse('password change', args=[user.pk, get_hash(user)])
			send_mail(
				'Смена пароля на ArtChart',
				'Для смены пароля перейдите по ссылке: ' + link,
				EMAIL_HOST_USER,
				[email]
			)
			message = 'Мы направили на ваш эл. адрес инструкции по смене пароля'
		except User.DoesNotExist:
			message = 'Произошла ошибка'

		return render(request, 'login/message.html', {'message': message})

	else:
		form = ACPasswordResetForm()
		return render(request, 'login/password reset.html', {'form': form})


def password_change(request, pk, hash):
	try:
		user = User.objects.get(pk = pk)

		if get_hash(user) != hash:
			message = 'Произошла ошибка. Возможно, ссылка для восстановления пароля устарела'
			return render(request, 'login/message.html', {'message': message})

		if request.method == 'POST':
			form = ACSetPasswordForm(user, request.POST)

			if form.is_valid():
				form.save()
				message = 'Пароль был успешно изменен'

			else:
				message = 'Произошла ошибка'

			return render(request, 'login/message.html', {'message': message})

		else:
			form = ACSetPasswordForm(user)
			return render(request, 'login/password change.html', {'form': form, 'hash': hash})

	except User.DoesNotExist:
		message = 'Произошла ошибка'
		return render(request, 'login/message.html', {'message': message})

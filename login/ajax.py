from django.contrib.auth.models import User
from django.http import HttpResponse


def check_nickname(request):
	name = request.GET['name']

	if User.objects.filter(username = name).exists():
		message = 'Это имя уже используется :('.format(name)
		return HttpResponse(message)

	return HttpResponse("")


def check_email(request):
	email = request.GET['email']

	if User.objects.filter(email = email).exists():
		message = 'Этот email уже используется'
		return HttpResponse(message)

	return HttpResponse("")

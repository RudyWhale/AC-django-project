from django.contrib.auth.models import User
from django.http import HttpResponse

def check_nickname(request):
	name = request.GET['name']

	if User.objects.filter(username = name).exists():
		message = 'Пользователь с именем {} уже зарегистрирован. Пожалуйста, выберите другое имя'.format(name)
		return HttpResponse(message)

	return HttpResponse("")

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as user_logout
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from main.models import ArtistProfile
from .forms import ArtistCreationForm, RegistrationForm

def register(request):
	if request.method == 'POST':
   		form = RegistrationForm(request.POST)
   		username = request.POST['username']
   		email = request.POST['email']
   		password = request.POST['password1']
   		password_repeat = request.POST['password2']

   		if User.objects.filter(username=username).exists():
   			message = 'Простите, пользователь с таким именем уже существует. Выберите, пожалуйста, другое имя.'
   			return render(request, 'login/register.html', {'form': form, 'message': message})

   		elif password != password_repeat:
   			message = 'Неверно повторен пароль'
   			return render(request, 'login/register.html', {'form': form, 'message': message})

   		else:
   			User.objects.create_user(username=username, password=password, email=email)
   			return redirect('login')

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
		# Takes care of user permissions
		reg_perm = Permission.objects.get(name="Can add artist profile")
		download_perm = Permission.objects.get(name="Can add publication")
		request.user.user_permissions.remove(reg_perm)
		request.user.user_permissions.add(download_perm)

		# creates new artist profile
		image = request.FILES.get('avatar')
		desc = request.POST.get('desc')
		ArtistProfile.objects.create(
			desc = desc,
			avatar = image,
			user = request.user
			)

		return redirect('index')

	else:
		if (request.user.has_perm('main.add_artistprofile')):
			form = ArtistCreationForm()
			return render(request, 'login/register as artist.html', {'form': form})
		else:
			return redirect('become_artist')

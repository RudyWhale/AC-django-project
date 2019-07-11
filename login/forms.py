from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import ArtistProfile
from django import forms
from django.utils.html import strip_tags


class RegistrationForm(UserCreationForm):
	username = forms.CharField(
		required = True,
		widget = forms.widgets.TextInput(attrs={'placeholder': 'Имя профиля', 'class': 'inp_name'})
	)
	email = forms.EmailField(
		required = True,
		widget = forms.widgets.EmailInput(attrs={'placeholder': 'Ваша действующая эл. почта', 'class': 'inp_email'})
	)
	password1 = forms.CharField(
		required = True,
		widget = forms.widgets.PasswordInput(attrs={'placeholder': 'Придумайте пароль', 'class': 'pass1'})
	)
	password2 = forms.CharField(
		required = True,
		widget = forms.widgets.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class': 'pass2'})
	)

	class Meta:
		model = User
		fields = ('username', 'email')


class ArtistCreationForm(forms.ModelForm):
	desc = forms.CharField(
		required = True,
		widget = forms.widgets.Textarea(attrs={'cols': '38', 'rows': '10'})
		)

	avatar = forms.ImageField(required=True)

	class Meta:
		model = ArtistProfile
		fields = ['desc', 'avatar']

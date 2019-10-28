from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from PIL import Image
from io import BytesIO
from datetime import datetime
from main.models import ArtistProfile
from main.widgets import LimitedLengthTextarea
from .snippets import get_hash
from ArtChart.settings import EMAIL_HOST_USER, PROFILE_AVATAR_MAX_SIZE as MAX_AVATAR_SIZE, PROFILE_DESC_MAX_LENGTH


'''
Form for ordinary user registration
'''
class RegistrationForm(UserCreationForm):
	password1 = forms.CharField(
		required = True,
		widget = forms.widgets.PasswordInput(attrs={'placeholder': 'Придумайте пароль', 'class': 'pass1'})
	)
	password2 = forms.CharField(
		required = True,
		widget = forms.widgets.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class': 'pass2'})
	)
	email = forms.CharField(
		required = True,
		widget = forms.widgets.EmailInput(attrs={'placeholder': 'Ваша действующая эл. почта', 'class': 'inp_email'})
	)

	class Meta:
		model = User
		fields = ['username']
		widgets = {'username': forms.widgets.TextInput(attrs={'placeholder': 'Имя профиля', 'class': 'inp_name'})}

	def clean_email(self):
		email = self.cleaned_data['email']
		validate_email(email)

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Email already used')

		return email

	def clean_password2(self):
		password = self.cleaned_data['password2']

		if len(password) < 6:
			raise forms.ValidationError('Password too short')

		return password

	def save(self, commit=True):
		user = super().save(commit = False)

		user.email = self.cleaned_data['email']
		user.is_active = False

		if commit:
			user.save()

		return user


'''
Form for artist registration
'''
class ArtistCreationForm(forms.ModelForm):
	desc_attrs = {
		'cols': '38',
		'rows': '7',
		'placeholder': 'Напишите о себе. Эта информация будет отображаться в вашем профиле',
		'maxlength': PROFILE_DESC_MAX_LENGTH,
		'class': 'limited_length'
	}
	desc = forms.CharField(
		required=True,
		widget=LimitedLengthTextarea(attrs=desc_attrs)
	)
	avatar = forms.ImageField(
		required=True,
		widget=forms.widgets.FileInput(attrs={'class': 'avatar_inp', 'data-max_size': MAX_AVATAR_SIZE})
	)

	class Meta:
		model = ArtistProfile
		fields = ['desc', 'avatar']

	def clean_avatar(self):
		file = self.cleaned_data['avatar']

		if file.size > MAX_AVATAR_SIZE:
			raise forms.ValidationError('Avatar is too big')

		return file

	def clean_desc(self):
		text = self.cleaned_data['desc']

		if len(text) > PROFILE_DESC_MAX_LENGTH:
			raise forms.ValidationError('Desc text is too long')

		return text

	def save(self, user, commit=True):
		profile = super().save(commit=False)

		profile.user = user

		if commit:
			profile.save()

		return profile


class ACPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(
		max_length=254,
		widget=forms.widgets.EmailInput(attrs={'placeholder': 'Введите ваш email'})
	)


class ACSetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите новый пароль'}))

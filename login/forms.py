from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.urls import reverse
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from main.models import ArtistProfile, BlackList
from main.widgets import LimitedLengthTextarea
from .snippets import get_hash
from ArtChart.settings import USE_RECAPTCHA


'''
Login form
'''
class ACAuthenticationForm(AuthenticationForm):
	username = forms.CharField(max_length=254, label="Имя")
	password = forms.CharField(label="Пароль", widget=forms.widgets.PasswordInput)
	if USE_RECAPTCHA:
		captcha = ReCaptchaField()


'''
Form for user registration
'''
class RegistrationForm(UserCreationForm):
	password1 = forms.CharField(
		required = True,
		widget = forms.widgets.PasswordInput(
			attrs={
				'placeholder': 'Придумайте пароль',
				'class': 'pass1',
				'autocomplete': 'off'
			}),
		label = 'Пароль'
	)
	password2 = forms.CharField(
		required = True,
		widget = forms.widgets.PasswordInput(
			attrs={
				'placeholder': 'Повторите пароль',
				'class': 'pass2',
				'autocomplete': 'off'
			}),
		label = 'Пароль'
	)
	email = forms.CharField(
		required = True,
		widget = forms.widgets.EmailInput(
			attrs={
				'placeholder': 'Ваша действующая эл. почта',
				'class': 'inp_email',
				'autocomplete': 'off'
			}),
		label = 'Почта'
	)
	username = forms.CharField(
		required = True,
		max_length = 254,
		label = 'Имя',
		widget = forms.widgets.TextInput(
			attrs={
				'placeholder': 'Имя профиля',
				'class': 'inp_name',
				'autocomplete': 'off'
			}),
	)
	if USE_RECAPTCHA:
		captcha = ReCaptchaField()


	class Meta:
		model = User
		fields = ['username', 'email']


	def clean_email(self):
		email = self.cleaned_data['email']
		validate_email(email)

		from main.models import BlackList

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Email already used')

		# Check if email not in blacklist
		if BlackList.objects.all():
			try:
				BlackList.objects.get(email=email)
				raise forms.ValidationError('Email in blacklist')
			except BlackList.DoesNotExist:
				pass

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


class ACPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(
		max_length=254,
		widget=forms.widgets.EmailInput(attrs={'placeholder': 'Введите ваш email'}),
		label='email',
	)


class ACSetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль', 'class': 'pass1'}),
		label='пароль',
	)
	new_password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': 'Повторите новый пароль', 'class': 'pass2'}),
		label='пароль',
	)


	def clean_new_password2(self):
		password = self.cleaned_data['new_password2']

		if len(password) < 6:
			raise forms.ValidationError('Password too short')

		return password

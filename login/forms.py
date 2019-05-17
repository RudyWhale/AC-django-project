from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import ArtistProfile
from django import forms
from django.utils.html import strip_tags


class RegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'email')


class ArtistCreationForm(forms.ModelForm):
	desc = forms.CharField(
		required=True,
		widget=forms.widgets.Textarea(attrs={'cols': "38", "rows": "10"})
		)

	avatar = forms.ImageField(required=True)

	class Meta:
		model = ArtistProfile
		fields = ['desc', 'avatar']
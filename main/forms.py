from django import forms
from django.forms import ModelForm
from PIL import Image
from datetime import datetime
from .models import Artwork, Tag, UserSettings, ArtistProfile, ArtworkCategory
from .widgets import LimitedLengthTextarea, ACCheckBox
from ArtChart.settings import ARTWORK_DESC_MAX_LENGTH, ARTWORK_IMAGE_MAX_SIZE, PROFILE_AVATAR_MAX_SIZE, PROFILE_DESC_MAX_LENGTH


class AbstractPostCreationForm(ModelForm):
    tag_set = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'placeholder': 'Впишите, теги, соответствующие, работе, разделив, их, запятой'}),
        label = 'Теги через запятую'
    )

    def save(self, profile, commit=True):
        post = super().save(commit=False)
        post.author = profile
        post.datetime = datetime.now()

        if commit:
            post.save()

        tags_str = self.cleaned_data['tag_set'].replace(" ", "").lower()

        for tag_name in tags_str.split(','):
            try:
                tag = Tag.objects.get(name = tag_name)

            except Tag.DoesNotExist:
                tag = Tag.objects.create(name = tag_name)

            tag.publications.add(post)

        return post


class ArtworkCreationForm(AbstractPostCreationForm):
    desc_textarea_attrs = {
        'placeholder': 'Напишите здесь о работе',
        'maxlength': ARTWORK_DESC_MAX_LENGTH,
        'class': 'limited_length'
    }
    desc = forms.CharField(
        required = True,
        widget = LimitedLengthTextarea(attrs=desc_textarea_attrs),
        label = 'Описание')
    image = forms.ImageField(
        required = True,
        widget = forms.widgets.FileInput(attrs={'class': 'image_inp', 'data-max_size': ARTWORK_IMAGE_MAX_SIZE}),
        label = 'Загрузите фотографию')
    name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={'placeholder': 'Придумайте название для работы'}),
        label = 'Название')
    category = forms.ModelChoiceField(
        required = False,
        queryset = ArtworkCategory.objects.all(),
        label='Выберите категорию'
    )

    class Meta:
        model = Artwork
        fields = ['name', 'desc', 'image', 'category']

    def clean_image(self):
        file = self.cleaned_data['image']

        if file.size > ARTWORK_IMAGE_MAX_SIZE:
            raise forms.ValidationError('Artwork image is too big')

        return file


class FeedbackForm(forms.Form):
    message_textarea_attrs = {
        'placeholder':  'Напишите ваше сообщение для администрации портала.' \
                        'Если нужно, укажите электронную почту или другие контакты для связи',
        'maxlength': '1000',
        'class': 'limited_length',
    }
    message = forms.CharField(
        required = True,
        widget = LimitedLengthTextarea(attrs=message_textarea_attrs),
        label = 'Ваше сообщение'
    )


class UserSettingsForm(forms.ModelForm):
    feed_update_notifications = forms.BooleanField(
        label = 'Лента',
        required = False,
        widget = ACCheckBox(label='Уведомлять вас, когда в ленте появляется что-то новое')
    )

    class Meta:
        model = UserSettings
        fields = ['feed_update_notifications',]


'''
Form for artist profile
'''
class ArtistProfileForm(forms.ModelForm):
	avatar = forms.ImageField(
		required=False,
		widget=forms.widgets.FileInput(attrs={'class': 'avatar_inp image_inp', 'data-max_size': PROFILE_AVATAR_MAX_SIZE}),
		label='Фото',
	)
	desc_attrs = {
		'cols': '38',
		'rows': '7',
		'placeholder': 'Напишите о себе. Эта информация будет отображаться в вашем профиле',
		'maxlength': PROFILE_DESC_MAX_LENGTH,
		'class': 'limited_length'
	}
	desc = forms.CharField(
		required=False,
		widget=LimitedLengthTextarea(attrs=desc_attrs),
		label='Описание',
	)


	class Meta:
		model = ArtistProfile
		fields = ['avatar', 'desc']


	def clean_avatar(self):
		file = self.cleaned_data['avatar']

		if file and file.size > PROFILE_AVATAR_MAX_SIZE:
			raise forms.ValidationError('Avatar is too big')

		return file


	def clean_desc(self):
		text = self.cleaned_data['desc']

		if len(text) > PROFILE_DESC_MAX_LENGTH:
			raise forms.ValidationError('Desc text is too long')

		return text

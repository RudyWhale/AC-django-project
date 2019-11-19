from django import forms
from django.forms import ModelForm
from PIL import Image
from datetime import datetime
from .models import Artwork, Tag, UserSettings, ProfileSettings
from .widgets import LimitedLengthTextarea
from ArtChart.settings import ARTWORK_DESC_MAX_LENGTH, ARTWORK_IMAGE_MAX_SIZE


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

    class Meta:
        model = Artwork
        fields = ['name', 'desc', 'image']

    def clean_image(self):
        file = self.cleaned_data['image']

        if file.size > ARTWORK_IMAGE_MAX_SIZE:
            raise forms.ValidationError('Artwork image is too big')

        return file


class FeedbackForm(forms.Form):
    message_textarea_attrs = {
        'placeholder': 'Напишите ваше сообщение для администрации портала. Если нужно, укажите электронную почту для связи',
        'maxlength': '1000',
        'class': 'limited_length',
    }
    message = forms.CharField(
        required = True,
        widget = LimitedLengthTextarea(attrs=message_textarea_attrs),
        label = 'Ваше сообщение'
    )


class UserSettingsForm(forms.Form):
    CHOICES = [('feed_update_notifications', 'Уведомлять об обновлениях вашей персональной ленты'),]
    email_settings = forms.ChoiceField(
        label = 'Email-уведомления',
        widget = forms.CheckboxSelectMultiple,
        choices = CHOICES
    )

    def __init__(self, user_settings, profile_settings=None):
        super().__init__()
        settings_field = self.fields['email_settings']
        settings_field.initial = ['feed_update_notifications' if user_settings.feed_update_notifications else None]

        if profile_settings:
            PROFILE_CHOICES = [
                ('subscribers_update_notifications', 'Уведомлять о новых подписчиках'),
                ('publication_comments_update_notifications', 'Уведомлять о новых комментариях к моим работам')
            ]
            settings_field.choices += PROFILE_CHOICES

            if profile_settings.subscribers_update_notifications:
                settings_field.initial.append('subscribers_update_notifications')

            if profile_settings.publication_comments_update_notifications:
                settings_field.initial.append('publication_comments_update_notifications')

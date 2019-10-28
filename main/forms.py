from django import forms
from django.forms import ModelForm
from PIL import Image
from datetime import datetime
from .models import Artwork, Tag
from .widgets import LimitedLengthTextarea
from ArtChart.settings import ARTWORK_DESC_MAX_LENGTH, ARTWORK_IMAGE_MAX_SIZE


class AbstractPostCreationForm(ModelForm):
    tag_set = forms.CharField(
        max_length = 50,
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

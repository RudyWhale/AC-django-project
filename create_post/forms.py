from django import forms
from django.forms import ModelForm
from PIL import Image
from datetime import datetime
from main.models import Artwork, Tag


class AbstractPostCreationForm(ModelForm):
    tag_set = forms.CharField(max_length=50,
                widget=forms.TextInput(attrs={'placeholder': 'Впишите, теги, соответствующие, работе, разделив, их, запятой'}))

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
    desc = forms.CharField(required = True,
                widget=forms.widgets.Textarea(attrs={'placeholder': 'Напишите здесь о работе'}))

    name = forms.CharField(required=True,
                widget=forms.TextInput(attrs={'placeholder': 'Придумайте название для работы'}))

    class Meta:
        model = Artwork
        fields = ['name', 'desc', 'image']

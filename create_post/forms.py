from django import forms
from django.forms import ModelForm
from main.models import Artwork, Article


class ArtworkCreationForm(ModelForm):
    tag_set = forms.CharField(max_length=50);

    class Meta:
        model = Artwork
        fields = ['name', 'desc', 'image']


class ArticleCreationForm(ModelForm):
    tag_set = forms.CharField(max_length=50);

    class Meta:
        model = Article
        fields = ['name', 'desc', 'text']

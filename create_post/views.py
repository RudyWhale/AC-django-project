from django.shortcuts import render
from .forms import ArtworkCreationForm, ArticleCreationForm
from datetime import datetime
from main.models import Artwork, Article, Tag
from django.shortcuts import redirect


def add_tags_to_publication(publication, tags_str):
    for tag_name in tags_str.split(','):
        try:
            tag = Tag.objects.get(name = tag_name)

        except Tag.DoesNotExist:
            tag = Tag.objects.create(name = tag_name)

        tag.publications.add(publication)


def new_artwork(request):
    user = request.user

    try:
        profile = user.profile
    except AttributeError as e:
        args = {
            'msg_header': "Ошибка доступа",
            'msg_text' : "Произошла ошибка. Возможно, вы вышли из своего аккаунта"
        }
        return render(request, 'main/info message.html', args)

    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        image = request.FILES.get('image')

        artwork = Artwork.objects.create(
            author = profile,
            date = datetime.now(),
            name = name,
            desc = desc,
            image = image
        )

        tag_str = request.POST['tag_set'].replace(" ", "").lower()
        add_tags_to_publication(artwork, tag_str)

        return redirect('artist', pk = profile.pk)
    else:
        form = ArtworkCreationForm()
        return render(request, 'create_post/artwork create.html', {'form': form})


def new_article(request):
    user = request.user

    try:
        profile = user.profile
    except AttributeError as e:
        args = {
            'msg_header': "Ошибка доступа",
            'msg_text' : "Произошла ошибка. Возможно, вы вышли из своего аккаунта"
        }
        return render(request, 'main/info message.html', args)

    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        text = request.POST['text']

        article = Article.objects.create(
            author = profile,
            date = datetime.now(),
            name = name,
            desc = desc,
            text = text
        )

        tag_str = request.POST['tag_set'].replace(" ", "").lower()
        add_tags_to_publication(article, tag_str)

        return redirect('artist', pk = profile.pk)
    else:
        form = ArticleCreationForm()
        return render(request, 'create_post/article create.html', {'form': form})

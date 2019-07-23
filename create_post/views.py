from django.shortcuts import render
from .forms import ArtworkCreationForm, ArticleCreationForm
from datetime import datetime
from main.models import Artwork, Article
from django.shortcuts import redirect


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
        # name = request.POST['name']
        # desc = request.POST['desc']
        # image = request.FILES.get('image')
        #
        # artwork = Artwork.objects.create(
        #     author = profile,
        #     date = datetime.now(),
        #     name = name,
        #     desc = desc,
        #     image = image
        # )
        #
        # tag_str = request.POST['tag_set'].replace(" ", "").lower()
        # add_tags_to_publication(artwork, tag_str)
        form = ArtworkCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(profile = profile)
            return redirect('artist', pk = profile.pk)

        else:
            args = {
                'msg_header': 'Ошибка',
                'msg_text': 'К сожалению, во время создания публикации прозошла ошибка. При повторении ошибки обратитесь к администрации сайта'
            }
            return render(request, 'main/info message.html', args)

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
        # name = request.POST['name']
        # desc = request.POST['desc']
        # text = request.POST['text']
        #
        # article = Article.objects.create(
        #     author = profile,
        #     date = datetime.now(),
        #     name = name,
        #     desc = desc,
        #     text = text
        # )
        #
        # tag_str = request.POST['tag_set'].replace(" ", "").lower()
        # add_tags_to_publication(article, tag_str)
        form = ArticleCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(profile = profile)
            return redirect('artist', pk = profile.pk)

        else:
            args = {
                'msg_header': 'Ошибка',
                'msg_text': 'К сожалению, во время создания публикации прозошла ошибка. При повторении ошибки обратитесь к администрации сайта'
            }
            return render(request, 'main/info message.html', args)

    else:
        form = ArticleCreationForm()
        return render(request, 'create_post/article create.html', {'form': form})

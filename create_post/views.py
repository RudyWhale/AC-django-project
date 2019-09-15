from django.shortcuts import render
from .forms import ArtworkCreationForm
from datetime import datetime
from main.models import Artwork
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

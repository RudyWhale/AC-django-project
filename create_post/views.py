from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ArtworkCreationForm
from main.models import Artwork
from ArtChart.settings import ARTWORK_DESC_MAX_LENGTH
from datetime import datetime


def new_artwork(request):
    user = request.user

    try:
        profile = user.profile
    except AttributeError as e: return HttpResponse(status=403)

    if request.method == 'POST':
        form = ArtworkCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(profile = profile)
            return redirect('artist', pk = profile.pk)

        else: return HttpResponse(status=400)

    else:
        form = ArtworkCreationForm()
        args = {
            'form': form,
            'max_desc_length': ARTWORK_DESC_MAX_LENGTH
        }
        return render(request, 'create_post/artwork create.html', args)

from django.utils import timezone
from functools import partial


# This method returns function which generates filenames for images
# We cannot use lambdas here because of specificity of django migrations
# This function used in main.models
def image_upload_path(obj, filename, dir):
	date = timezone.now()
	return f"{dir}/{date.year}/{date.month}/{str(obj.pk)}.{filename.split('.')[-1].lower()}"

def get_image_upload_path(dir):
    return partial(image_upload_path, dir=dir)

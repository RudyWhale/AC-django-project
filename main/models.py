from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string


class UserSettings(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	feed_update_notifications = models.BooleanField(default=True)


class ArtistProfile(models.Model):
	def avatar_upload_path(self, filename):
		date = timezone.now()
		return 'avatars/{}/{}/{}'.format(date.year, date.month, filename)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	desc = models.TextField(default ='no desc')
	avatar = models.ImageField(upload_to=avatar_upload_path, blank=True)
	subscribers = models.ManyToManyField(User, related_name='subscriptions')

	def __str__(self):
		return self.user.username

	def as_html(self, user):
		return render_to_string('main/includes/artist overview.html', {'profile': self, 'user': user})


class ProfileSettings(models.Model):
	profile = models.OneToOneField(ArtistProfile, on_delete=models.CASCADE)
	subscribers_update_notifications = models.BooleanField(default=False)
	publication_comments_update_notifications = models.BooleanField(default=True)


# Abstract class for any publication
class Publication(models.Model):
	author = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
	datetime = models.DateTimeField()
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name


class Artwork(Publication):
	def upload_path(self, filename):
		date = timezone.now()
		return 'artworks/{}/{}/{}.{}'.format(date.year, date.month, str(self.pk), filename.split('.')[-1])

	desc = models.TextField(default='no desc')
	image = models.ImageField(upload_to=upload_path)

	def as_html(self):
		return render_to_string('main/includes/content item artwork.html', {'artwork': self})


class Comment(models.Model):
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField()
	text = models.TextField()

	def __str__(self):
		return self.author.username + ' on publication ' + str(self.publication.pk) + ': ' + self.text

	class Meta:
		ordering = ['-datetime']


class Tag(models.Model):
	name = models.CharField(max_length=30)
	publications = models.ManyToManyField(Publication)

	def __str__(self):
		return self.name

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string


# Settings attached to any registrated user
class UserSettings(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	feed_update_notifications = models.BooleanField(default=True)


def image_upload_path(obj, filename, dir):
	date = timezone.now()
	return f"{dir}/{date.year}/{date.month}/{str(obj.pk)}.{filename.split('.')[-1].lower()}"


# Additional data of user, who can add publications
class ArtistProfile(models.Model):
	avatar_upload_path = lambda self, filename : image_upload_path(self, filename, dir='avatars')
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	desc = models.TextField(default ='')
	avatar = models.ImageField(upload_to=avatar_upload_path, default='avatars/default.png')
	subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True)

	def __str__(self):
		return self.user.username

	def as_html(self, user):
		return render_to_string('main/page_blocks/artist overview.html', {'profile': self, 'user': user})


# Abstract class for any publication
class Publication(models.Model):
	author = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
	datetime = models.DateTimeField()
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name


# Is this publication traditional artwork, photo or digital art?
class ArtworkCategory(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name


class Artwork(Publication):
	artwork_upload_path = lambda self, filename : image_upload_path(self, filename, dir='artworks')
	desc = models.TextField(default='no desc')
	image = models.ImageField(upload_to=artwork_upload_path)
	category = models.ForeignKey(ArtworkCategory, on_delete=models.SET_NULL, null=True)

	def as_html(self):
		return render_to_string('main/includes/content item artwork.html', {'artwork': self})


# Publication comments
class Comment(models.Model):
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField()
	text = models.TextField()

	def __str__(self):
		return self.author.username + ' on publication ' + str(self.publication.pk) + ': ' + self.text

	class Meta:
		ordering = ['-datetime']


# Replies to comments
class Reply(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField()
	text = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

	def __str__(self):
		return self.author.username + ' on comment ' + str(self.comment.pk) + ': ' + self.text

	class Meta:
		ordering = ['datetime']


# Publication tags. Names are unique, lowercased and contain no spaces
class Tag(models.Model):
	name = models.CharField(max_length=30)
	publications = models.ManyToManyField(Publication)

	def __str__(self):
		return self.name


# This model keeps information about updates in user's feed
class NewInFeed(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	publications = models.ManyToManyField(Publication)


'''
Web notifications
-----------------
Notify user about related events in navbar
'''
class WebNotification(models.Model):
	recipient = models.ForeignKey(User, on_delete=models.CASCADE)


class CommentWebNotification(WebNotification):
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class ReplyWebNotification(WebNotification):
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE)


class SubscriberWebNotification(WebNotification):
	subscriber = models.ForeignKey(User, on_delete=models.CASCADE)


class LikesWebNotification(WebNotification):
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User)


# Task for sending email notification asynchronously
class BaseEmailTask(models.Model):
	recipient = models.ForeignKey(User, on_delete=models.CASCADE)


# Keeps info about new publications in user's personal feed
class FeedUpdateEmailTask(BaseEmailTask):
	publications = models.ManyToManyField(Publication)


class BlackList(models.Model):
	email = models.EmailField()
	comment = models.CharField(max_length=1000, blank=True)

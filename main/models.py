from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


'''
Class represents user who can create publications
'''
class ArtistProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	desc = models.TextField(default='no desc')
	avatar = models.ImageField(upload_to='avatars', blank=True)
	subscribers = models.ManyToManyField(User, related_name='subscriptions')

	def __str__(self):
		return self.user.username


'''
Abstract class for any publication
'''
class Publication(models.Model):
	author = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
	date = models.DateTimeField()
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name


'''
Class represents artwork publication object
'''
class Artwork(Publication):
	desc = models.TextField(default='no desc')
	image = models.ImageField(upload_to='artworks')


'''
Class represents an article publication object
'''
class Article(Publication):
	desc = models.TextField(default='no desc')
	text = models.TextField(default='no text')


class Comment(models.Model):
	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField()
	text = models.TextField()

	def __str__(self):
		return self.author.username + ' on publication ' + str(self.publication.pk) + ': ' + self.text

	class Meta:
		ordering = ['-date']


class Tag(models.Model):
	name = models.CharField(max_length=30)
	publications = models.ManyToManyField(Publication)

	def __str__(self):
		return self.name

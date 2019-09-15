from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string


'''
Class represents user who can create publications
'''
class ArtistProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	desc = models.TextField(default ='no desc')
	avatar = models.ImageField(upload_to='avatars', blank=True)
	subscribers = models.ManyToManyField(User, related_name='subscriptions')

	def __str__(self):
		return self.user.username


'''
Abstract class for any publication
'''
class Publication(models.Model):
	author = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
	datetime = models.DateTimeField()
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

	# def as_json(self):
	# 	return {
	# 			"author_pk": self.author.pk,
	# 			"datestamp": self.datetime.timestamp(),
	# 			"likes": self.likes,
	# 			"name": self.name,
	# 			"desc": self.desc,
	# 			"image_url": self.image.url
	# 		}

	def as_html(self):
		return render_to_string('main/includes/content item artwork.html', {'artwork': self})


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

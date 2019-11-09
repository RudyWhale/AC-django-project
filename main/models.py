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


'''
=============================== RECEIVERS ===============================
'''
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from ArtChart.settings import EMAIL_HOST_USER, HOST
import os


# Deletes avatar file after profile deleting
@receiver(post_delete, sender=ArtistProfile)
def on_instance_delete(sender, instance, **kwargs):
	if instance.avatar:
		if os.path.isfile(instance.avatar.path):
			os.remove(instance.avatar.path)


# Deletes image file after instance deleting
@receiver(post_delete, sender=Artwork)
def on_instance_delete(sender, instance, **kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)


@receiver(post_save, sender=Artwork)
def notify_subs(sender, instance, created, **kwargs):
	if created:
		author = instance.author
		subs = author.subscribers.exclude(usersettings__feed_update_notifications=False)
		settings_url = reverse('settings')
		url = HOST + reverse('artwork', args=(instance.pk,))
		text = 'В вашей персональной ленте на ArtChart появилась новая работа. Чтобы увидеть ее, перейдите по ссылке: ' + url
		html = render_to_string('email_templates/feed_update_notification.html', {'link': url})

		for user in subs:
			send_mail(
				f'Новая публикация от {author.user.username} в вашей ленте на ArtChart!',
				text,
				EMAIL_HOST_USER,
				[user.email,],
				html_message = html
			)


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
	pub_author_profile = instance.publication.author
	pub_author = pub_author_profile.user
	commentator = instance.author

	if created and pub_author_profile.profilesettings.publication_comments_update_notifications and commentator != pub_author:
		publication = instance.publication
		url = HOST + reverse('artwork', args=(publication.pk,))
		theme = 'Новый комментарий к вашей работе на ArtChart'
		text = f'Пользователь {commentator.username} написал новый комментарий к вашей работе {publication.name} на ArtChart. ' \
				f'Перейдите по ссылке: {url}, чтобы увидеть страницу публикации'
		args = {
			'author': commentator.username,
			'publication': publication,
			'link': url,
		}
		html = render_to_string('email_templates/new_comment_notification.html', args)
		send_mail(
			theme,
			text,
			EMAIL_HOST_USER,
			[pub_author.email],
			html_message = html,
		)

from django.db.models.signals import post_delete, pre_save, post_save, post_init, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.signals import request_finished
from django.contrib.auth.models import User
from main.models import *
import os


# Resize artwork or avatar image
from PIL import Image
def resize_image(path, size, crop=False):
	image = Image.open(path)
	width, height = image.size

	if crop:
		padding = abs(width - height) / 2

		if width >= height:
			box = (padding, 0, width-padding, height)
		else:
			box = (0, padding, width, height-padding)

		image = image.crop(box)

	image.thumbnail(size)
	image.save(path)


# Deletes avatar file after profile deleting
@receiver(post_delete, sender=ArtistProfile)
def on_profile_delete(sender, instance, **kwargs):
	# Taken from https://djangosnippets.org/snippets/10638/
	if instance.avatar:
		if os.path.isfile(instance.avatar.path):
			os.remove(instance.avatar.path)


# Deletes avatar when profile changed
@receiver(pre_save, sender=ArtistProfile)
def delete_avatar_when_changed(sender, instance, **kwargs):
	# Taken from https://djangosnippets.org/snippets/10638/
	if not instance.pk:
		return False

	try:
		old_file = sender.objects.get(pk=instance.pk).avatar
	except sender.DoesNotExist:
		return False

	if old_file:
		new_file = instance.avatar

		if not old_file == new_file:
			if os.path.isfile(old_file.path):
				os.remove(old_file.path)


# After avatar loaded to server resize it to keep more space on disk
from ArtChart.settings import AVATAR_SIZE

@receiver(post_save, sender=ArtistProfile)
def resize_avatar(sender, instance, **kwargs):
	if instance.avatar:
		if os.path.isfile(instance.avatar.path):
			resize_image(instance.avatar.path, AVATAR_SIZE, crop=True)


# Deletes image file after instance deleting
@receiver(post_delete, sender=Artwork)
def on_artwork_delete(sender, instance, **kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)


# Creates email task for artist's subscribers or adds new publication to task
@receiver(post_save, sender=Artwork)
def notify_subs(sender, instance, created, **kwargs):
	if created:
		recipients = instance.author.subscribers.exclude(usersettings__feed_update_notifications=False)

		for user in recipients:
			email_task = FeedUpdateEmailTask.objects.get_or_create(recipient=user)[0]
			email_task.publications.add(instance)
			email_task.save()


# Resize artwork image after loading to keep more space on disk
from ArtChart.settings import ARTWORK_SIZE

@receiver(post_save, sender=Artwork)
def resize_artwork(sender, instance, **kwargs):
	resize_image(instance.image.path, ARTWORK_SIZE)


'''
Web notifications handlers
--------------------------
Notify user about related events in navbar
'''
@receiver(m2m_changed, sender=ArtistProfile.subscribers.through)
def subscriber_notify(sender, instance, action, **kwargs):
	if action == 'post_add' and len(kwargs['pk_set']) == 1:
		SubscriberWebNotification.objects.get_or_create(
			recipient=instance.user,
			subscriber=User.objects.get(pk__in=kwargs['pk_set'])
		)


@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, created, **kwargs):
	if created and instance.author != instance.publication.author.user:
		CommentWebNotification.objects.create(
			recipient=instance.publication.author.user,
			comment=instance
		)


@receiver(post_save, sender=Reply)
def reply_notify(sender, instance, created, **kwargs):
	if created and instance.author != instance.comment.author:
		ReplyWebNotification.objects.create(
			recipient=instance.comment.author,
			reply=instance
		)


@receiver(m2m_changed, sender=Publication.likes.through)
def likes_notify(sender, instance, action, **kwargs):
	if action=='post_add' and len(kwargs['pk_set'])==1 and instance.author.user.pk not in kwargs['pk_set']:
		notification = LikesWebNotification.objects.get_or_create(
			recipient=instance.author.user,
			publication=instance
		)[0]
		notification.likes.add(*User.objects.filter(pk__in=kwargs['pk_set']))


@receiver(post_save, sender=Artwork)
def update_newinfeed_objects(sender, instance, created, **kwargs):
	if created:
		subs = instance.author.subscribers.all()

		for user in subs:
			new_in_feed = NewInFeed.objects.get_or_create(user=user)[0]
			new_in_feed.publications.add(instance)
			new_in_feed.save()

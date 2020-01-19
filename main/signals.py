from django.db.models.signals import post_delete, pre_save, post_save, post_init
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.signals import request_finished
from django.contrib.auth.models import User
from main.models import ArtistProfile, Artwork, Comment, FeedUpdateEmailTask, WebNotification, CommentWebNotification
import os


# Deletes avatar file after profile deleting
@receiver(post_delete, sender=ArtistProfile)
def on_profile_delete(sender, instance, **kwargs):
	# Taken from https://djangosnippets.org/snippets/10638/
	if instance.avatar:
		if os.path.isfile(instance.avatar.path):
			os.remove(instance.avatar.path)


@receiver(pre_save, sender=ArtistProfile)
def delete_avatar_when_changed(sender, instance, **kwargs):
	# Taken from https://djangosnippets.org/snippets/10638/
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


# Deletes image file after instance deleting
@receiver(post_delete, sender=Artwork)
def on_artwork_delete(sender, instance, **kwargs):
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)


# Notifies user about new comment in navbar
@receiver(post_save, sender=Comment)
def comment_notify(sender, instance, created, **kwargs):
	if created and instance.author != instance.publication.author.user:
		CommentWebNotification.objects.create(
			recipient=instance.publication.author.user,
			comment=instance
		)


'''
Email tasks for sending email notification asynchronously
'''
# Creates email task for artist's subscribers or adds new publication to task
@receiver(post_save, sender=Artwork)
def notify_subs(sender, instance, created, **kwargs):
	if created:
		recipients = instance.author.subscribers.exclude(usersettings__feed_update_notifications=False)

		for user in recipients:
			email_task = FeedUpdateEmailTask.objects.get_or_create(recipient=user)[0]
			email_task.publications.add(instance)
			email_task.save()

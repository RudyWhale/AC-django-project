from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from main.models import ArtistProfile, Artwork, Comment, FeedUpdateEmailTask
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


# @receiver(post_save, sender=Comment)
# def notify_comment(sender, instance, created, **kwargs):
# 	if created:
# 		profile = instance.publication.author
# 		recipient = profile.user
# 		commentator = instance.author
#
# 		if profile.profilesettings.publication_comments_update_notifications and commentator != recipient:
# 			email_task = CommentsEmailTask.objects.get_or_create(recipient=recipient)[0]
# 			email_task.comments.add(instance)
# 			email_task.save()
#
#
# @receiver(m2m_changed, sender=ArtistProfile.subscribers.through)
# def notify_subscriber(sender, instance, action, pk_set, **kwargs):
# 	if action == "post_add" and instance.profilesettings.subscribers_update_notifications:
# 		recipient = instance.user
# 		subscriber = User.objects.filter(pk__in=pk_set)[0]
#
# 		email_task = SubscribersEmailTask.objects.get_or_create(recipient=recipient)[0]
# 		email_task.subscribers.add(subscriber)
# 		email_task.save()

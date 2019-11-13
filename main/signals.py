from django.db.models.signals import post_delete, pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from ArtChart.settings import EMAIL_HOST_USER, HOST
from main.models import ArtistProfile, Artwork, Comment
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
		settings_url = HOST + reverse('settings')
		text = 'В вашей персональной ленте на ArtChart появилась новая работа. Чтобы увидеть ее, перейдите по ссылке: ' + url
		html = render_to_string('email_templates/feed_update_notification.html', {'link': url, 'settings_url': settings_url})

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
		settings_url = HOST + reverse('settings')
		theme = 'Новый комментарий к вашей работе на ArtChart'
		text = f'Пользователь {commentator.username} написал новый комментарий к вашей работе {publication.name} на ArtChart. ' \
				f'Перейдите по ссылке: {url}, чтобы увидеть страницу публикации'
		args = {
			'author': commentator.username,
			'publication': publication,
			'link': url,
			'settings_url': settings_url,
		}
		html = render_to_string('email_templates/new_comment_notification.html', args)
		send_mail(
			theme,
			text,
			EMAIL_HOST_USER,
			[pub_author.email],
			html_message = html,
		)


@receiver(m2m_changed, sender=ArtistProfile.subscribers.through)
def notify_subscriber(sender, instance, action, pk_set, **kwargs):
	if action == "post_add":
		subscriber = User.objects.filter(pk__in=pk_set)[0]
		url = HOST + reverse('artist', args=(instance.pk,))
		settings_url = HOST + reverse('settings')
		theme = 'У вас новый подписчик на ArtChart'
		text = f'Пользователь {subscriber.username} подпсался на ваш профиль на ArtChart. ' \
				f'Вы можете перейти в профиль по ссылке: {url}'
		args = {
			'subscriber': subscriber.username,
		 	'link': url,
			'settings_url': settings_url,
		}
		html = render_to_string('email_templates/new_subscriber_notification.html', args)
		send_mail(
			theme,
			text,
			EMAIL_HOST_USER,
			[instance.user.email],
			html_message = html,
		)

from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from ArtChart.settings import EMAIL_HOST_USER, HOST
from main.models import FeedUpdateEmailTask


def run():
    tasks = FeedUpdateEmailTask.objects.all()

    for task in tasks:
        # Check if publications list is empty
        if task.publications.exists():
            theme = "Что-то новое появилось в вашей ленте на ArtChart!"
            args = {
                'task': task,
                'settings_url': HOST + reverse('settings'),
                'feed_url': HOST + reverse('feed')
            }
            html = render_to_string('email_templates/feed_update_notification.html', args)
            text = "В вашей персональной ленте на ArtChart появилось что-то новое! " \
                    f"Вы можете посмотреть свою ленту, перейдя по ссылке: {HOST}/{reverse('feed')}" \
                    "\nЕсли хотите отписаться от таких уведомлений, можете перейти на страницу настроек по ссылке: " \
                    f"{HOST}/{reverse('settings')}"

            send_mail(theme, text, EMAIL_HOST_USER, (task.recipient.email,), html_message=html)

        task.delete()

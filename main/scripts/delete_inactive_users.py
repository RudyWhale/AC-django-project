from django.contrib.auth.models import User
from datetime import datetime, timedelta


def run():
    # Delete account if it is not activated longer than 1 day
    User.objects.filter(is_active=False, date_joined__lt=(datetime.now() - timedelta(1))).delete()

# Generated by Django 2.1.3 on 2019-12-18 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_blacklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

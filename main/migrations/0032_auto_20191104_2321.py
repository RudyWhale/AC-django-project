# Generated by Django 2.1.3 on 2019-11-04 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20191104_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilesettings',
            name='subscribers_update_notifications',
            field=models.BooleanField(default=False),
        ),
    ]
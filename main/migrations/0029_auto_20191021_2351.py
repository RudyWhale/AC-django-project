# Generated by Django 2.1.3 on 2019-10-21 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20190925_0939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-datetime']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='date',
            new_name='datetime',
        ),
    ]
# Generated by Django 2.1.3 on 2019-05-06 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20190506_1711'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.DateTimeField(),
        ),
    ]

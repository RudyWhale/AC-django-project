# Generated by Django 2.1.3 on 2019-07-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20190726_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='name',
            field=models.CharField(default='no name', max_length=250),
        ),
    ]
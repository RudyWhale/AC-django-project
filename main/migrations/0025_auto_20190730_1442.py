# Generated by Django 2.1.3 on 2019-07-30 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20190730_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='publication',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]

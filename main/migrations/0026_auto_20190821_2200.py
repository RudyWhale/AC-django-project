# Generated by Django 2.1.3 on 2019-08-21 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20190730_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractarticleblock',
            name='article',
        ),
        migrations.RemoveField(
            model_name='article',
            name='publication_ptr',
        ),
        migrations.RemoveField(
            model_name='textarticleblock',
            name='abstractarticleblock_ptr',
        ),
        migrations.AlterField(
            model_name='artistprofile',
            name='desc',
            field=models.TextField(default='no desc'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='desc',
            field=models.TextField(default='no desc'),
        ),
        migrations.DeleteModel(
            name='AbstractArticleBlock',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='TextArticleBlock',
        ),
    ]
# Generated by Django 2.1.3 on 2019-07-26 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_remove_article_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractArticleBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TextArticleBlock',
            fields=[
                ('abstractarticleblock_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.AbstractArticleBlock')),
                ('text', models.TextField()),
            ],
            bases=('main.abstractarticleblock',),
        ),
        migrations.AddField(
            model_name='abstractarticleblock',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Article'),
        ),
    ]
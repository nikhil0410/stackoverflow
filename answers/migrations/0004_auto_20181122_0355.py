# Generated by Django 2.1.3 on 2018-11-22 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0003_answerscomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='total_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answerscomment',
            name='total_count',
            field=models.IntegerField(default=0),
        ),
    ]
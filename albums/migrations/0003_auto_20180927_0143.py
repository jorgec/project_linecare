# Generated by Django 2.1.1 on 2018-09-27 01:43

import albums.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_album_album_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(max_length=512, upload_to=albums.models.photo_upload_path),
        ),
    ]
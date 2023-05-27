# Generated by Django 4.1.6 on 2023-05-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OceanApp', '0002_asset'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tag',
            field=models.CharField(default='#blog', max_length=200),
        ),
        migrations.AlterField(
            model_name='asset',
            name='video',
            field=models.CharField(default='img_video/video.mp4', max_length=100),
        ),
    ]
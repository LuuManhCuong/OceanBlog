# Generated by Django 4.1.6 on 2023-05-24 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OceanApp', '0013_remove_comment_author_remove_comment_idcoment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='OceanApp.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='idComent',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='OceanApp.blog'),
        ),
    ]

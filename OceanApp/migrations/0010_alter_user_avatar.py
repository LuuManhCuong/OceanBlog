# Generated by Django 4.1.6 on 2023-05-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OceanApp', '0009_blog_author_alter_blog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(default='https://img.freepik.com/premium-vector/female-user-profile-avatar-is-woman-character-screen-saver-with-emotions_505620-617.jpg', max_length=500),
        ),
    ]

# Generated by Django 3.2.18 on 2023-06-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]

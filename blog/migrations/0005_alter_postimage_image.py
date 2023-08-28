# Generated by Django 3.2.18 on 2023-07-12 14:07

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(upload_to=blog.models.generate_image_filename),
        ),
    ]
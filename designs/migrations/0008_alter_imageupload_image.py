# Generated by Django 4.2.7 on 2023-11-28 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0007_alter_imageupload_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='image',
            field=models.ImageField(upload_to='media/uploaded'),
        ),
    ]

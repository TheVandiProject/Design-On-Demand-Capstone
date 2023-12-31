# Generated by Django 4.2.5 on 2023-11-14 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploaded/')),
            ],
        ),
        migrations.AlterField(
            model_name='uploaddesign',
            name='image',
            field=models.ImageField(upload_to='media/uploaded'),
        ),
    ]

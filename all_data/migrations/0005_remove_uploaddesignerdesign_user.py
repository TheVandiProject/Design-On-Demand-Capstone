# Generated by Django 4.2.7 on 2023-12-03 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('all_data', '0004_category_uploaddesignerdesign_designer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploaddesignerdesign',
            name='user',
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-30 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0011_alter_category_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DesignProduct',
        ),
    ]

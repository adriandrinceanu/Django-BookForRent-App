# Generated by Django 5.0.1 on 2024-01-29 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_lib', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Author',
            new_name='author',
        ),
    ]

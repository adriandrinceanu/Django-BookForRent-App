# Generated by Django 5.0.1 on 2024-01-31 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_lib', '0012_recenzie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recenzie',
            name='titlu',
            field=models.CharField(max_length=100),
        ),
    ]

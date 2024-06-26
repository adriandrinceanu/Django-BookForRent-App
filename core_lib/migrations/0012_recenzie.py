# Generated by Django 5.0.1 on 2024-01-31 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_lib', '0011_alter_book_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recenzie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1)),
                ('titlu', models.CharField(max_length=10)),
                ('descriere', models.CharField(max_length=100)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_lib.book')),
            ],
        ),
    ]

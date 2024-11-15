# Generated by Django 5.1.3 on 2024-11-13 04:02

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangomanager', '0002_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('A', 'Author'), ('E', 'Editor')], max_length=1)),
            ],
            managers=[
                ('people', django.db.models.manager.Manager()),
            ],
        ),
    ]

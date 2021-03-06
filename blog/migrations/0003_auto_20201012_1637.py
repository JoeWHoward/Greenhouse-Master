# Generated by Django 3.1.2 on 2020-10-12 21:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20201008_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='presentation',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Post date'),
        ),
    ]

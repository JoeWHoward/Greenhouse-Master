# Generated by Django 3.1.2 on 2020-10-13 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_author_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='role',
            field=models.CharField(default='Plant Expert', max_length=20, verbose_name='Role (eg. Plant Expert)'),
        ),
    ]

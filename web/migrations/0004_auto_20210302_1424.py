# Generated by Django 3.1.6 on 2021-03-02 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20210223_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-23 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_password',
            field=models.CharField(max_length=200),
        ),
    ]

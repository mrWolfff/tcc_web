# Generated by Django 2.2.2 on 2019-08-18 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='categoria_user',
        ),
    ]

# Generated by Django 2.2.2 on 2019-08-25 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_categoria_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='categoria_categoria',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='data_nascimento_user',
        ),
    ]
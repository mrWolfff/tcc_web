# Generated by Django 2.2.2 on 2019-11-28 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_auto_20191104_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_proposta',
            field=models.BooleanField(default=False),
        ),
    ]

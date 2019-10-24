# Generated by Django 2.2.2 on 2019-10-14 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0003_auto_20191013_0132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['time_message']},
        ),
        migrations.CreateModel(
            name='Propostas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposta', models.TextField()),
                ('valor_proposta', models.CharField(blank=True, max_length=20, null=True)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('to_user_proposta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_proposta', to=settings.AUTH_USER_MODEL)),
                ('user_proposta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_proposta', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

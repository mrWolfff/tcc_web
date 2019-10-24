# Generated by Django 2.2.2 on 2019-10-21 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0004_auto_20191014_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicos',
            name='descricao_servico',
        ),
        migrations.RemoveField(
            model_name='servicos',
            name='requisitos_servico',
        ),
        migrations.RemoveField(
            model_name='servicos',
            name='titulo_servico',
        ),
        migrations.AddField(
            model_name='servicos',
            name='proposta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='principal.Propostas'),
        ),
        migrations.AddField(
            model_name='servicos',
            name='status',
            field=models.CharField(max_length=240, null=True),
        ),
    ]

# Generated by Django 2.2.2 on 2019-08-20 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_demandas_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicos_Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria_servico', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='demandas',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='principal.Servicos_Categoria'),
        ),
    ]

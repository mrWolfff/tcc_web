# Generated by Django 2.2.4 on 2019-12-04 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_avaliacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='imagem',
            field=models.ImageField(blank=True, default='https://miro.medium.com/max/3200/1*g09N-jl7JtVjVZGcd-vL2g.jpeg', null=True, upload_to='user_images/'),
        ),
        migrations.AlterField(
            model_name='servicos_categoria',
            name='imagem',
            field=models.ImageField(upload_to=''),
        ),
    ]

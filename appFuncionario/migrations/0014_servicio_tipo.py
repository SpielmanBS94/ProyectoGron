# Generated by Django 3.2.9 on 2021-12-06 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFuncionario', '0013_cliente_fotoperfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='tipo',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

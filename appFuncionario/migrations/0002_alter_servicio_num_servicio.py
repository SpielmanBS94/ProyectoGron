# Generated by Django 3.2.9 on 2021-11-29 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFuncionario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='num_servicio',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]

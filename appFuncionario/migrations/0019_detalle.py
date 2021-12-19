# Generated by Django 3.2.9 on 2021-12-19 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFuncionario', '0018_auto_20211217_0235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id_detalle', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_hora_entrega', models.DateTimeField(null=True)),
                ('fecha_hora_entrega_real', models.DateTimeField(null=True)),
                ('bici', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='appFuncionario.bicicleta')),
                ('epp', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='appFuncionario.epp')),
                ('est', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='appFuncionario.estacionamiento')),
                ('herr', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='appFuncionario.herramienta')),
                ('servicio', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='appFuncionario.servicio')),
            ],
        ),
    ]

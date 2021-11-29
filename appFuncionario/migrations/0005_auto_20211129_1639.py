# Generated by Django 3.2.9 on 2021-11-29 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFuncionario', '0004_alter_servicio_funcionario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarjeta',
            name='codigo',
        ),
        migrations.AlterField(
            model_name='servicio',
            name='Cliente',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='appFuncionario.cliente'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='Funcionario',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='appFuncionario.funcionario'),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='numero_tarjeta',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
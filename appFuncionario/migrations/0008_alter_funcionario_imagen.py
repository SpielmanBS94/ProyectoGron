# Generated by Django 3.2.9 on 2021-12-04 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFuncionario', '0007_funcionario_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='imagen',
            field=models.ImageField(null=True, upload_to='funcionarios/imagenPerfil/'),
        ),
    ]

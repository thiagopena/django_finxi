# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-31 16:47
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django_finxi.apps.main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_curta', models.CharField(max_length=32)),
                ('descricao', models.CharField(blank=True, max_length=1055, null=True)),
                ('tipo', models.CharField(choices=[('R', 'Residencial'), ('C', 'Comercial'), ('U', 'Rural'), ('O', 'Outro')], max_length=1)),
                ('imobiliaria', models.CharField(blank=True, max_length=32, null=True)),
                ('foto', models.ImageField(blank=True, default='imagens/default.png', upload_to=django_finxi.apps.main.models.img_directory_path)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('area', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('rua', models.CharField(blank=True, max_length=255, null=True)),
                ('numero', models.CharField(blank=True, max_length=16, null=True)),
                ('bairro', models.CharField(blank=True, max_length=64, null=True)),
                ('regiao', models.CharField(blank=True, max_length=36, null=True)),
                ('complemento', models.CharField(blank=True, max_length=64, null=True)),
                ('pais', models.CharField(blank=True, default='Brasil', max_length=32, null=True)),
                ('municipio', models.CharField(blank=True, max_length=64, null=True)),
                ('cep', models.CharField(blank=True, max_length=16, null=True)),
                ('uf', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('EX', 'EX'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
            ],
        ),
    ]

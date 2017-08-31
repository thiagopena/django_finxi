# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver

from decimal import Decimal
import os
import uuid

import locale
locale.setlocale(locale.LC_ALL, '')


UF_SIGLA = [
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('EX', 'EX'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
]

TIPO_IMOVEL = [
    ('R', 'Residencial'),
    ('C', 'Comercial'),
    ('U', 'Rural'),
    ('O', 'Outro'),
]


def img_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return 'imagens/imoveis/imovel_{0}{1}'.format(str(uuid.uuid4()), extension)


class Imovel(models.Model):
    descricao_curta = models.CharField(max_length=32)
    descricao = models.CharField(max_length=1055, null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=TIPO_IMOVEL)
    imobiliaria = models.CharField(max_length=32, null=True, blank=True)
    foto = models.ImageField(upload_to=img_directory_path,
                             default='imagens/default.png', blank=True)
    valor = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    area = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                               MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=16, null=True, blank=True)
    bairro = models.CharField(max_length=64, null=True, blank=True)
    regiao = models.CharField(max_length=36, null=True, blank=True)
    complemento = models.CharField(max_length=64, null=True, blank=True)
    pais = models.CharField(max_length=32, null=True,
                            blank=True, default='Brasil')
    municipio = models.CharField(max_length=64, null=True, blank=True)
    cep = models.CharField(max_length=16, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True,
                          blank=True, choices=UF_SIGLA)

    @property
    def format_valor(self):
        if self.valor:
            return 'R$ {}'.format(locale.format(u'%.2f', self.valor, 1))
        else:
            return '----'

    @property
    def format_area(self):
        if self.area:
            return '{}m²'.format(locale.format(u'%.2f', self.valor, 1))
        else:
            return '----'

    @property
    def format_municipio(self):
        if self.municipio:
            return self.municipio
        else:
            return '----'

    @property
    def format_bairro(self):
        if self.bairro:
            return self.bairro
        else:
            return '----'

    def save(self, *args, **kwargs):
        # Deletar foto se ja existe
        try:
            obj = Imovel.objects.get(id=self.id)
            if obj.foto != self.foto and obj.foto != 'imagens/default.png':
                obj.foto.delete(save=False)
        except Imovel.DoesNotExist:
            pass
        super(Imovel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.descricao_curta

    def __str__(self):
        return self.descricao_curta


@receiver(post_delete, sender=Imovel)
def foto_post_delete_handler(sender, instance, **kwargs):
    # Nao deletar a imagem default
    if instance.foto != 'imagens/default.png':
        instance.foto.delete(False)

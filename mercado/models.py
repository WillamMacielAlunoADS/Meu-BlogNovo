from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length = 200)
    preco_uni = models.FloatField()
    estoque = models.IntegerField()
    liquido = models.FloatField(null=True)

    def __str__(self):
        return self.nome

class Compra(models.Model):
    cod_compra = models.IntegerField()
    codigo_prod = models.IntegerField(null=True)
    produtos = models.CharField(max_length = 1000, null=True, blank=True)
    total = models.FloatField()

    def __str__(self):
        return self.cod_compra


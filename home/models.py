from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ColaModel(models.Model):
    class Meta:
        verbose_name="Cola"
        verbose_name_plural="Colas"
    codigo = models.AutoField(primary_key=True)
    nombre_de_la_cola = models.CharField(max_length=200,blank=False,null=False)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE,blank=False,null=False,editable=False)
    usuarios_acceso = models.ManyToManyField(User, related_name="Usuarios_con_acceso")

class ColaItem(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
    codigo = models.AutoField(primary_key=True)
    cola = models.ForeignKey(ColaModel, on_delete=models.CASCADE,blank=False,null=False,editable=False)
    nombre = models.CharField(max_length=200,blank=False,null=False)
    apellidos = models.CharField(max_length=200)
    numero = models.IntegerField(blank=True,null=True)
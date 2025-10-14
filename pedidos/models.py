from django.db import models

class Categoria(models.Model):
    id_categoria = models.BigAutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
    imagen_cat = models.ImageField(upload_to='pedidos/images/')

class Producto(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pedidos/images/')
    price = models.IntegerField()
    disponible = models.BooleanField(default=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
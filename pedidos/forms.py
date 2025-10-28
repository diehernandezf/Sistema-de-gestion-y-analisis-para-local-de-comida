from django import forms
from .models import Producto, Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre_categoria", "imagen_cat"]   # ajusta a tus campos reales

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["name", "description", "image", "price", "disponible"]
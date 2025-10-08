from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

def home(request):
    products = Producto.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, post_id):
    product = get_object_or_404(Producto, pk=post_id)
    return render(request, 'product_detail.html', {'product': product})

def products(request, id_categoria):
    categoria = get_object_or_404(Categoria, pk=id_categoria)
    productos = Producto.objects.filter(id_categoria=categoria)
    return render(request, 'products.html', {'products': productos, 'categoria':categoria})

def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})
from django.shortcuts import redirect, render, get_object_or_404
from .models import Producto, Categoria
from pedidos.carrito import Carrito

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



def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("products:productos", id_categoria=producto.id_categoria_id)

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("products:productos", {'producto':producto})

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("products:productos", id_categoria=producto.id_categoria_id) # la ruta productos tambien lleva un id, asique debemos pasarle el id
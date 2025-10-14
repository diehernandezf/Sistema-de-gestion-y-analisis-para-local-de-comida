from django.urls import path
from .views import products, product_detail, categorias, agregar_producto, eliminar_producto, restar_producto

app_name = 'products'

urlpatterns = [
    path('', categorias, name='categorias'),
    path('<int:id_categoria>/', products, name='productos'),
    path('agregar/<int:producto_id>/', agregar_producto, name='add'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='del'),
    path('restar/<int:producto_id>/', restar_producto, name='sub'),
]
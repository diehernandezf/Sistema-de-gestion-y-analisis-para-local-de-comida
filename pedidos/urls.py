from django.urls import path
from .views import products, categorias, agregar_producto, restar_producto, paypal_crear_orden, paypal_capturar_orden, CrearOrden, CapturarOrdernPaypal, vaciar_carrito, crudProducto
app_name = 'products'

urlpatterns = [
    path('', categorias, name='categorias'),
    path('<int:id_categoria>/', products, name='productos'),
    path('agregar/<int:producto_id>/', agregar_producto, name='add'),
    path('vaciar/<int:id_categoria>', vaciar_carrito, name='limpiar'),
    path('restar/<int:producto_id>/', restar_producto, name='sub'),
    path('crud/', crudProducto, name='crud'),
    path('api/orders', CrearOrden.as_view()),
    path('api/orders/<str:order_id>/capture/', CapturarOrdernPaypal.as_view(), name='api_capture_order'),
]
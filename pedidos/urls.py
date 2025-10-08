from django.urls import path
from .views import products, product_detail, categorias

app_name = 'products'

urlpatterns = [
    path('', categorias, name='categorias'),
    path('<int:id_categoria>/', products, name='productos')
]
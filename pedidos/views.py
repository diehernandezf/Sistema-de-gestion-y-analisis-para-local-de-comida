from email import message
import json
from django.shortcuts import redirect, render, get_object_or_404
from .models import Producto, Categoria
from pedidos.carrito import Carrito

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from .functions import get_paypal_client

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .functions import get_paypal_client

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CategoriaForm, ProductoForm

def home(request):
    products = Producto.objects.all()
    return render(request, 'home.html', {'products': products})

def products(request, id_categoria):
    categoria = get_object_or_404(Producto, pk=id_categoria)
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
    producto = Producto.objects.filter(id=producto_id).first()
    if not producto:
        removed = carrito.eliminar(producto)
        if removed:
            message.info(request, 'Este producto ya no existe y fue retirado del carrito')
        return redirect("products:categorias")
    carrito.restar(producto)
    return redirect("products:productos", id_categoria=producto.id_categoria_id) # la ruta productos tambien lleva un id, asique debemos pasarle el id

def vaciar_carrito(request, id_categoria):
    if "carrito" in request.session:
        del request.session["carrito"]
        request.session.modified = True
    return redirect("products:productos", id_categoria=id_categoria)

def crudProducto(request):
    productos = Producto.objects.all()
    return render(request, 'crudProductos.html', {'productos': productos})

@csrf_exempt  
def paypal_crear_orden(request):
    try:
        carrito = Carrito(request)
        total = 0
        for item in carrito.carrito.values():
            total += float(item["total"])

        if total <= 0:
            # 🔴 Antes: HttpResponseBadRequest("...") (texto)
            # ✅ Ahora: siempre JSON
            return JsonResponse({"error": "Carrito vacío o total inválido"}, status=400)

        client = get_paypal_client()
        req = OrdersCreateRequest()
        req.prefer('return=representation')
        req.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": f"{total:.2f}",
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": f"{total:.2f}"
                        }
                    }
                }
            }]
        })

        resp = client.execute(req)
        return JsonResponse({"id": resp.result.id}, status=200)

    except Exception as e:
        # 🔴 Antes: HttpResponseServerError(str(e)) (texto)
        # ✅ Ahora: JSON
        return JsonResponse({"error": str(e)}, status=500)
    




@csrf_exempt                     # para pruebas rápidas con fetch(); en prod envía CSRF
@require_POST
def paypal_capturar_orden(request, order_id):
    """
    Captura una orden aprobada por el comprador.
    """
    try:
        client = get_paypal_client()
        req = OrdersCaptureRequest(order_id)
        req.request_body({})  # body vacío según el SDK
        resp = client.execute(req)

        # Aquí puedes marcar el pedido como pagado en tu DB,
        # limpiar carrito, enviar correo, etc.
        return JsonResponse({
            "status": resp.result.status,
            "id": resp.result.id,
            "payer": getattr(resp.result, "payer", None) and {
                "name": resp.result.payer.name.given_name,
                "email": resp.result.payer.email_address,
            }
        })
    except Exception as e:
        return HttpResponseServerError(str(e))





@method_decorator(csrf_exempt, name='dispatch')
class CrearOrden(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        carrito = Carrito(request)
        total = 0
        for item in carrito.carrito.values():
            total += float(item["total"])

        if total <= 0:
            # 🔴 Antes: HttpResponseBadRequest("...") (texto)
            # ✅ Ahora: siempre JSON
            return JsonResponse({"error": "Carrito vacío o total inválido"}, status=400)

        client = get_paypal_client()
        req = OrdersCreateRequest()
        req.prefer("return=representation")
        req.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": f"{total:.2f}",
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": f"{total:.2f}"
                        }
                    }
                }
            }]
        })
        resp = client.execute(req)
        return Response({"id": resp.result.id}, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class CapturarOrdernPaypal(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print("TYPE", type(request), "ORDER_ID", locals().get("order_id"))

        order = paypal_crear_orden(request)
        data = json.loads(order.content.decode("utf-8"))

        try:
            order_id = self.kwargs['order_id']
            response = paypal_capturar_orden(order_id)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response({'error': 'algun error'}, status=status.HTTP_400_BAD_REQUEST)
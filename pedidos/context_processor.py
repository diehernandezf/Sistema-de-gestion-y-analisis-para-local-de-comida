def total_carrito(request):
    total = 0
    if "carrito" in request.session:
        for _, value in request.session["carrito"].items():
            try:
                total += int(value.get("total", 0))   # admite int o "5300"
            except (TypeError, ValueError):
                # Fallback: si no existe 'total', calcula price * cantidad (enteros)
                try:
                    total += int(value.get("price", 0)) * int(value.get("cantidad", 0))
                except (TypeError, ValueError):
                    continue
    return {"total_carrito": total}

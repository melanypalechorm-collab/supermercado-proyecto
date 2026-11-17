from persistencia import cargar_datos, guardar_datos

ARCHIVO_PROD = 'productos.json'
ARCHIVO_VENTAS = 'ventas.json'
ARCHIVO_CAJA = 'caja.json'

def inicializar():
    cargar_datos(ARCHIVO_PROD, {})
    cargar_datos(ARCHIVO_VENTAS, [])
    cargar_datos(ARCHIVO_CAJA, {"saldo_inicial": 0, "movimientos": []})

def registrar_producto(codigo, nombre, categoria, p_compra, p_venta, stock, stock_min):
    productos = cargar_datos(ARCHIVO_PROD, {})
    if codigo in productos:
        raise ValueError("El código ya existe.")
    if float(p_venta) < 0 or float(p_compra) < 0:
        raise ValueError("Los precios no pueden ser negativos.")
        
    productos[codigo] = {
        "nombre": nombre, "categoria": categoria,
        "precio_compra": float(p_compra), "precio_venta": float(p_venta),
        "stock": int(stock), "stock_minimo": int(stock_min)
    }
    guardar_datos(ARCHIVO_PROD, productos)

def obtener_productos():
    return cargar_datos(ARCHIVO_PROD, {})

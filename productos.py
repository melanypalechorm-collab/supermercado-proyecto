import json
from pathlib import Path

ARCHIVO = Path(__file__).parent / "datos" / "productos.json"


def cargar_productos():
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

    if not ARCHIVO.exists():
        ARCHIVO.write_text("[]", encoding="utf-8")
        return []

    contenido = ARCHIVO.read_text(encoding="utf-8").strip()

    if contenido == "":
        return []

    return json.loads(contenido)


def guardar_productos(productos):
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)


def registrar_producto():
    productos = cargar_productos()

    print("\n--- REGISTRO DE PRODUCTOS ---")

    codigo = input("Codigo del producto: ").upper()

    for producto in productos:
        if producto["codigo"] == codigo:
            print("Error: Este codigo ya existe.")
            return

    nombre = input("Nombre del producto: ")
    categoria = input("Categoria: ")

    try:
        precio_compra = float(input("Precio de compra: "))
        precio_venta = float(input("Precio de venta: "))
        stock = int(input("Cantidad disponible: "))
        stock_minimo = int(input("Stock minimo: "))

        if precio_compra < 0 or precio_venta < 0 or stock < 0 or stock_minimo < 0:
            print("Error: No se permiten valores negativos.")
            return

    except ValueError:
        print("Error: Debe ingresar valores numericos validos.")
        return

    nuevo_producto = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "precio_compra": precio_compra,
        "precio_venta": precio_venta,
        "stock": stock,
        "stock_minimo": stock_minimo
    }

    productos.append(nuevo_producto)
    guardar_productos(productos)

    print("\nProducto registrado correctamente.")


def mostrar_productos():
    productos = cargar_productos()

    print("\n--- LISTA DE PRODUCTOS ---")

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        print("--------------------------")
        print("Codigo:", producto["codigo"])
        print("Nombre:", producto["nombre"])
        print("Categoria:", producto["categoria"])
        print("Precio de compra:", producto["precio_compra"])
        print("Precio de venta:", producto["precio_venta"])
        print("Stock:", producto["stock"])
        print("Stock minimo:", producto["stock_minimo"])


def menu_productos():
    while True:
        print("\n--- GESTION DE PRODUCTOS ---")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "0":
            break
        else:
            print("Opcion incorrecta.")
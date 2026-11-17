import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path
import json

from productos import cargar_productos, guardar_productos



CARPETA_DATOS = Path(__file__).parent / "datos"

ARCHIVO_VENTAS = CARPETA_DATOS / "ventas.json"
ARCHIVO_DEVOLUCIONES = CARPETA_DATOS / "devoluciones.json"
ARCHIVO_CAJA = CARPETA_DATOS / "caja.json"

VERDE = "#174d38"
VERDE_CLARO = "#287653"
FONDO = "#f1f5f2"
BLANCO = "#ffffff"
ROJO = "#b83232"

CARPETA_DATOS.mkdir(exist_ok=True)


def cargar_datos(ruta):
    if not ruta.exists():
        ruta.write_text("[]", encoding="utf-8")
        return []

    contenido = ruta.read_text(encoding="utf-8").strip()

    if not contenido:
        return []

    return json.loads(contenido)


def guardar_datos(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def dinero(valor):
    return f"${valor:,.2f}"


# ==========================================
# VENTANA PRINCIPAL
# ==========================================

ventana = tk.Tk()
ventana.title("Supermercado Mi Tienda")
ventana.geometry("1150x700")
ventana.minsize(900, 600)
ventana.configure(bg=FONDO)

menu = tk.Frame(ventana, bg=VERDE, width=230)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

contenido = tk.Frame(ventana, bg=FONDO)
contenido.pack(side="right", fill="both", expand=True, padx=25, pady=25)

tk.Label(
    menu,
    text="🛒 MI TIENDA",
    bg=VERDE,
    fg=BLANCO,
    font=("Arial", 21, "bold")
).pack(pady=30)


def limpiar_contenido():
    for widget in contenido.winfo_children():
        widget.destroy()


def titulo_pagina(texto, descripcion=""):
    tk.Label(
        contenido,
        text=texto,
        bg=FONDO,
        fg=VERDE,
        font=("Arial", 23, "bold")
    ).pack(anchor="w", pady=(5, 5))

    if descripcion:
        tk.Label(
            contenido,
            text=descripcion,
            bg=FONDO,
            fg="#66756b",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(0, 15))


def crear_tabla(parent, columnas, encabezados, altura=12):
    tabla = ttk.Treeview(
        parent,
        columns=columnas,
        show="headings",
        height=altura
    )

    for columna, encabezado in zip(columnas, encabezados):
        tabla.heading(columna, text=encabezado)
        tabla.column(columna, width=125, anchor="center")

    tabla.pack(fill="both", expand=True, pady=10)
    return tabla


# ==========================================
# INICIO
# ==========================================

def inicio():
    limpiar_contenido()
    titulo_pagina(
        "Panel principal",
        "Bienvenido al sistema de gestión de Supermercado Mi Tienda."
    )

    productos = cargar_productos()
    ventas = cargar_datos(ARCHIVO_VENTAS)

    total_productos = len(productos)
    unidades = sum(p["stock"] for p in productos)
    stock_bajo = sum(
        1 for p in productos
        if p["stock"] <= p["stock_minimo"]
    )
    total_ventas = sum(v["total"] for v in ventas)

    tarjetas = tk.Frame(contenido, bg=FONDO)
    tarjetas.pack(fill="x", pady=25)

    datos = [
        ("Productos registrados", total_productos),
        ("Unidades en inventario", unidades),
        ("Productos con stock bajo", stock_bajo),
        ("Ventas acumuladas", dinero(total_ventas))
    ]

    for nombre, valor in datos:
        tarjeta = tk.Frame(
            tarjetas,
            bg=BLANCO,
            padx=15,
            pady=20,
            highlightbackground="#dce5df",
            highlightthickness=1
        )
        tarjeta.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            tarjeta,
            text=nombre,
            bg=BLANCO,
            fg="#66756b",
            font=("Arial", 10)
        ).pack()

        tk.Label(
            tarjeta,
            text=str(valor),
            bg=BLANCO,
            fg=VERDE_CLARO,
            font=("Arial", 19, "bold")
        ).pack(pady=10)

    tk.Label(
        contenido,
        text="Selecciona una opción del menú para comenzar.",
        bg=FONDO,
        fg="#66756b",
        font=("Arial", 13)
    ).pack(anchor="w", pady=20)


# ==========================================
# GESTIÓN DE PRODUCTOS
# ==========================================

def gestion_productos():
    limpiar_contenido()
    titulo_pagina(
        "Gestión de productos",
        "Registra, consulta y elimina productos del supermercado."
    )

    formulario = tk.LabelFrame(
        contenido,
        text="Registrar producto",
        bg=BLANCO,
        padx=12,
        pady=12
    )
    formulario.pack(fill="x", pady=8)

    campos = [
        ("Código", "codigo"),
        ("Nombre", "nombre"),
        ("Categoría", "categoria"),
        ("Precio de compra", "precio_compra"),
        ("Precio de venta", "precio_venta"),
        ("Cantidad disponible", "stock"),
        ("Stock mínimo", "stock_minimo")
    ]

    entradas = {}

    for i, (etiqueta, clave) in enumerate(campos):
        fila = i // 2
        columna = (i % 2) * 2

        tk.Label(
            formulario,
            text=etiqueta,
            bg=BLANCO
        ).grid(row=fila, column=columna, padx=6, pady=6, sticky="w")

        entrada = tk.Entry(formulario, width=23)
        entrada.grid(row=fila, column=columna + 1, padx=6, pady=6)
        entradas[clave] = entrada

    def registrar():
        codigo = entradas["codigo"].get().strip().upper()
        nombre = entradas["nombre"].get().strip()
        categoria = entradas["categoria"].get().strip()

        if not codigo or not nombre or not categoria:
            messagebox.showwarning(
                "Campos incompletos",
                "Completa el código, nombre y categoría."
            )
            return

        try:
            precio_compra = float(entradas["precio_compra"].get())
            precio_venta = float(entradas["precio_venta"].get())
            stock = int(entradas["stock"].get())
            stock_minimo = int(entradas["stock_minimo"].get())

            if min(precio_compra, precio_venta, stock, stock_minimo) < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Datos incorrectos",
                "Ingresa números válidos y no negativos."
            )
            return

        productos = cargar_productos()

        if any(p["codigo"] == codigo for p in productos):
            messagebox.showerror(
                "Código repetido",
                "Ese código ya existe."
            )
            return

        productos.append({
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio_compra": precio_compra,
            "precio_venta": precio_venta,
            "stock": stock,
            "stock_minimo": stock_minimo
        })

        guardar_productos(productos)

        messagebox.showinfo(
            "Correcto",
            "Producto registrado correctamente."
        )

        gestion_productos()

    tk.Button(
        formulario,
        text="Guardar producto",
        command=registrar,
        bg=VERDE_CLARO,
        fg=BLANCO,
        padx=12,
        pady=7
    ).grid(row=4, column=1, pady=8)

    tk.Label(
        contenido,
        text="Productos registrados",
        bg=FONDO,
        fg=VERDE,
        font=("Arial", 16, "bold")
    ).pack(anchor="w", pady=8)

    tabla = crear_tabla(
        contenido,
        ("codigo", "nombre", "categoria", "compra", "venta", "stock"),
        ("Código", "Nombre", "Categoría", "Compra", "Venta", "Stock"),
        8
    )

    for p in cargar_productos():
        tabla.insert(
            "",
            "end",
            values=(
                p["codigo"],
                p["nombre"],
                p["categoria"],
                dinero(p["precio_compra"]),
                dinero(p["precio_venta"]),
                p["stock"]
            )
        )

    def eliminar():
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Selecciona un producto de la tabla."
            )
            return

        valores = tabla.item(seleccion[0], "values")
        codigo = valores[0]

        confirmar = messagebox.askyesno(
            "Eliminar producto",
            f"¿Deseas eliminar {valores[1]}?"
        )

        if confirmar:
            productos = cargar_productos()
            productos = [
                p for p in productos
                if p["codigo"] != codigo
            ]

            guardar_productos(productos)
            messagebox.showinfo(
                "Correcto",
                "Producto eliminado."
            )
            gestion_productos()

    tk.Button(
        contenido,
        text="Eliminar producto seleccionado",
        command=eliminar,
        bg=ROJO,
        fg=BLANCO,
        padx=12,
        pady=8
    ).pack(anchor="e", pady=8)


# ==========================================
# INVENTARIO
# ==========================================

def modulo_inventario():
    limpiar_contenido()
    titulo_pagina(
        "Inventario",
        "Consulta las existencias y los productos que necesitan reposición."
    )

    tabla = crear_tabla(
        contenido,
        ("codigo", "nombre", "categoria", "stock", "minimo", "estado"),
        ("Código", "Producto", "Categoría", "Existencias", "Stock mínimo", "Estado")
    )

    productos = cargar_productos()

    for p in productos:
        estado = (
            "Stock bajo"
            if p["stock"] <= p["stock_minimo"]
            else "Disponible"
        )

        tabla.insert(
            "",
            "end",
            values=(
                p["codigo"],
                p["nombre"],
                p["categoria"],
                p["stock"],
                p["stock_minimo"],
                estado
            )
        )

    tk.Label(
        contenido,
        text=f"Total de productos: {len(productos)}",
        bg=FONDO,
        fg=VERDE,
        font=("Arial", 12, "bold")
    ).pack(anchor="e", pady=8)


# ==========================================
# VENTAS
# ==========================================

def modulo_ventas():
    limpiar_contenido()
    titulo_pagina(
        "Realizar ventas",
        "Selecciona los productos, agrega cantidades y finaliza la venta."
    )

    productos = cargar_productos()

    if not productos:
        tk.Label(
            contenido,
            text="Primero debes registrar productos.",
            bg=FONDO,
            fg=ROJO
        ).pack(pady=20)
        return

    carrito = []

    formulario = tk.LabelFrame(
        contenido,
        text="Agregar producto",
        bg=BLANCO,
        padx=12,
        pady=12
    )
    formulario.pack(fill="x", pady=10)

    tk.Label(formulario, text="Producto:", bg=BLANCO).grid(row=0, column=0)

    selector = ttk.Combobox(
        formulario,
        values=[
            f'{p["codigo"]} - {p["nombre"]}'
            for p in productos
        ],
        state="readonly",
        width=35
    )
    selector.grid(row=0, column=1, padx=8)

    tk.Label(formulario, text="Cantidad:", bg=BLANCO).grid(row=0, column=2)

    entrada_cantidad = tk.Entry(formulario, width=10)
    entrada_cantidad.grid(row=0, column=3, padx=8)
    entrada_cantidad.insert(0, "1")

    tabla = crear_tabla(
        contenido,
        ("codigo", "nombre", "precio", "cantidad", "subtotal"),
        ("Código", "Producto", "Precio", "Cantidad", "Subtotal"),
        10
    )

    total_label = tk.Label(
        contenido,
        text="TOTAL: $0.00",
        bg=FONDO,
        fg=VERDE,
        font=("Arial", 20, "bold")
    )
    total_label.pack(anchor="e", pady=10)

    def actualizar_carrito():
        tabla.delete(*tabla.get_children())
        total = 0

        for item in carrito:
            tabla.insert(
                "",
                "end",
                values=(
                    item["codigo"],
                    item["nombre"],
                    dinero(item["precio"]),
                    item["cantidad"],
                    dinero(item["subtotal"])
                )
            )
            total += item["subtotal"]

        total_label.config(text=f"TOTAL: {dinero(total)}")

    def agregar():
        if not selector.get():
            messagebox.showwarning(
                "Atención",
                "Selecciona un producto."
            )
            return

        try:
            unidades = int(entrada_cantidad.get())
            if unidades <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "La cantidad debe ser un entero mayor que cero."
            )
            return

        codigo = selector.get().split(" - ")[0]
        producto = next(
            (p for p in productos if p["codigo"] == codigo),
            None
        )

        if producto is None:
            return

        existente = next(
            (p for p in carrito if p["codigo"] == codigo),
            None
        )

        cantidad_actual = existente["cantidad"] if existente else 0

        if cantidad_actual + unidades > producto["stock"]:
            messagebox.showerror(
                "Inventario insuficiente",
                f"Solo hay {producto['stock']} unidades disponibles."
            )
            return

        if existente:
            existente["cantidad"] += unidades
            existente["subtotal"] = (
                existente["cantidad"] * existente["precio"]
            )
        else:
            carrito.append({
                "codigo": codigo,
                "nombre": producto["nombre"],
                "precio": producto["precio_venta"],
                "cantidad": unidades,
                "subtotal": producto["precio_venta"] * unidades,
                "devuelto": 0
            })

        actualizar_carrito()

    def finalizar():
        if not carrito:
            messagebox.showwarning(
                "Atención",
                "El carrito está vacío."
            )
            return

        productos_actuales = cargar_productos()

        for item in carrito:
            producto = next(
                (p for p in productos_actuales if p["codigo"] == item["codigo"]),
                None
            )

            if producto is None or producto["stock"] < item["cantidad"]:
                messagebox.showerror(
                    "Error",
                    f"No hay suficientes existencias de {item['nombre']}."
                )
                return

        for item in carrito:
            producto = next(
                p for p in productos_actuales
                if p["codigo"] == item["codigo"]
            )
            producto["stock"] -= item["cantidad"]

        guardar_productos(productos_actuales)

        total = round(sum(item["subtotal"] for item in carrito), 2)

        venta = {
            "id": "V" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [dict(item) for item in carrito],
            "total": total
        }

        ventas = cargar_datos(ARCHIVO_VENTAS)
        ventas.append(venta)
        guardar_datos(ARCHIVO_VENTAS, ventas)

        movimientos = cargar_datos(ARCHIVO_CAJA)
        movimientos.append({
            "fecha": venta["fecha"],
            "tipo": "Entrada",
            "concepto": f'Venta {venta["id"]}',
            "valor": total
        })
        guardar_datos(ARCHIVO_CAJA, movimientos)

        messagebox.showinfo(
            "Venta realizada",
            f'Venta: {venta["id"]}\nTotal: {dinero(total)}'
        )

        modulo_ventas()

    tk.Button(
        formulario,
        text="Agregar al carrito",
        command=agregar,
        bg=VERDE_CLARO,
        fg=BLANCO,
        padx=10,
        pady=6
    ).grid(row=0, column=4, padx=8)

    tk.Button(
        contenido,
        text="FINALIZAR VENTA",
        command=finalizar,
        bg=VERDE,
        fg=BLANCO,
        font=("Arial", 11, "bold"),
        padx=18,
        pady=10
    ).pack(anchor="e")


# ==========================================
# FACTURACIÓN
# ==========================================

def modulo_facturacion():
    limpiar_contenido()
    titulo_pagina(
        "Facturación",
        "Consulta las ventas y genera el comprobante de una venta."
    )

    ventas = cargar_datos(ARCHIVO_VENTAS)

    if not ventas:
        tk.Label(
            contenido,
            text="No hay ventas registradas.",
            bg=FONDO,
            fg=ROJO
        ).pack(pady=20)
        return

    tk.Label(
        contenido,
        text="Selecciona una venta:",
        bg=FONDO
    ).pack(anchor="w")

    selector = ttk.Combobox(
        contenido,
        values=[
            f'{v["id"]} - {v["fecha"]}'
            for v in ventas
        ],
        state="readonly",
        width=50
    )
    selector.pack(anchor="w", pady=10)

    area = tk.Text(
        contenido,
        height=20,
        width=75,
        font=("Courier New", 10)
    )
    area.pack(fill="both", expand=True, pady=10)

    def generar():
        if not selector.get():
            messagebox.showwarning(
                "Atención",
                "Selecciona una venta."
            )
            return

        venta_id = selector.get().split(" - ")[0]
        venta = next(
            (v for v in ventas if v["id"] == venta_id),
            None
        )

        if venta is None:
            return

        area.delete("1.0", tk.END)

        lineas = [
            "          SUPERMERCADO MI TIENDA",
            "              FACTURA DE VENTA",
            "----------------------------------------------",
            f'Factura: {venta["id"]}',
            f'Fecha: {venta["fecha"]}',
            "----------------------------------------------",
            "PRODUCTO             CANT.       SUBTOTAL",
            "----------------------------------------------"
        ]

        for item in venta["items"]:
            subtotal = item["subtotal"]
            lineas.append(
                f'{item["nombre"][:18]:18} '
                f'{item["cantidad"]:>5} '
                f'{dinero(subtotal):>15}'
            )

        lineas.extend([
            "----------------------------------------------",
            f'TOTAL: {dinero(venta["total"])}',
            "----------------------------------------------",
            "       Gracias por su compra."
        ])

        area.insert(tk.END, "\n".join(lineas))

    def guardar_factura():
        texto = area.get("1.0", tk.END).strip()

        if not texto:
            messagebox.showwarning(
                "Atención",
                "Primero consulta una factura."
            )
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
            title="Guardar factura"
        )

        if ruta:
            Path(ruta).write_text(texto, encoding="utf-8")
            messagebox.showinfo(
                "Factura guardada",
                "El comprobante se guardó correctamente."
            )

    botones = tk.Frame(contenido, bg=FONDO)
    botones.pack(anchor="w")

    tk.Button(
        botones,
        text="Consultar factura",
        command=generar,
        bg=VERDE_CLARO,
        fg=BLANCO,
        padx=12,
        pady=8
    ).pack(side="left", padx=5)

    tk.Button(
        botones,
        text="Guardar factura",
        command=guardar_factura,
        bg=VERDE,
        fg=BLANCO,
        padx=12,
        pady=8
    ).pack(side="left", padx=5)


# ==========================================
# DEVOLUCIONES
# ==========================================

def modulo_devoluciones():
    limpiar_contenido()
    titulo_pagina(
        "Devoluciones",
        "Registra productos devueltos de ventas anteriores."
    )

    ventas = cargar_datos(ARCHIVO_VENTAS)

    if not ventas:
        tk.Label(
            contenido,
            text="Todavía no hay ventas registradas.",
            bg=FONDO,
            fg=ROJO
        ).pack(pady=20)
        return

    formulario = tk.LabelFrame(
        contenido,
        text="Registrar devolución",
        bg=BLANCO,
        padx=20,
        pady=20
    )
    formulario.pack(fill="x", pady=15)

    tk.Label(
        formulario,
        text="Número de venta:",
        bg=BLANCO
    ).pack(anchor="w")

    selector_venta = ttk.Combobox(
        formulario,
        values=[v["id"] for v in ventas],
        state="readonly",
        width=45
    )
    selector_venta.pack(anchor="w", pady=8)

    tk.Label(
        formulario,
        text="Producto:",
        bg=BLANCO
    ).pack(anchor="w")

    selector_producto = ttk.Combobox(
        formulario,
        state="readonly",
        width=45
    )
    selector_producto.pack(anchor="w", pady=8)

    tk.Label(
        formulario,
        text="Cantidad a devolver:",
        bg=BLANCO
    ).pack(anchor="w")

    entrada_cantidad = tk.Entry(formulario, width=15)
    entrada_cantidad.pack(anchor="w", pady=8)
    entrada_cantidad.insert(0, "1")

    def actualizar_productos(event=None):
        venta_id = selector_venta.get()

        venta = next(
            (v for v in ventas if v["id"] == venta_id),
            None
        )

        if venta:
            disponibles = [
                f'{p["codigo"]} - {p["nombre"]}'
                for p in venta["items"]
                if p["cantidad"] - p.get("devuelto", 0) > 0
            ]

            selector_producto["values"] = disponibles
            selector_producto.set("")

    selector_venta.bind(
        "<<ComboboxSelected>>",
        actualizar_productos
    )

    def registrar_devolucion():
        venta_id = selector_venta.get()
        producto_seleccionado = selector_producto.get()

        if not venta_id or not producto_seleccionado:
            messagebox.showwarning(
                "Atención",
                "Selecciona una venta y un producto."
            )
            return

        try:
            unidades = int(entrada_cantidad.get())
            if unidades <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "Ingresa una cantidad válida."
            )
            return

        ventas_actuales = cargar_datos(ARCHIVO_VENTAS)
        productos_actuales = cargar_productos()

        venta = next(
            (v for v in ventas_actuales if v["id"] == venta_id),
            None
        )

        if venta is None:
            messagebox.showerror("Error", "Venta no encontrada.")
            return

        codigo = producto_seleccionado.split(" - ")[0]

        item = next(
            (p for p in venta["items"] if p["codigo"] == codigo),
            None
        )

        if item is None:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        disponibles = item["cantidad"] - item.get("devuelto", 0)

        if unidades > disponibles:
            messagebox.showerror(
                "Error",
                f"Solo puedes devolver {disponibles} unidades."
            )
            return

        producto = next(
            (p for p in productos_actuales if p["codigo"] == codigo),
            None
        )

        if producto is None:
            messagebox.showerror(
                "Error",
                "El producto no está en el inventario. No se puede actualizar su existencia."
            )
            return

        item["devuelto"] = item.get("devuelto", 0) + unidades
        producto["stock"] += unidades

        guardar_productos(productos_actuales)
        guardar_datos(ARCHIVO_VENTAS, ventas_actuales)

        valor_reembolso = round(item["precio"] * unidades, 2)

        devoluciones = cargar_datos(ARCHIVO_DEVOLUCIONES)
        devoluciones.append({
            "venta": venta_id,
            "codigo": codigo,
            "nombre": item["nombre"],
            "cantidad": unidades,
            "valor": valor_reembolso,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        guardar_datos(ARCHIVO_DEVOLUCIONES, devoluciones)

        movimientos = cargar_datos(ARCHIVO_CAJA)
        movimientos.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": "Salida",
            "concepto": f"Devolución de {venta_id}",
            "valor": valor_reembolso
        })
        guardar_datos(ARCHIVO_CAJA, movimientos)

        messagebox.showinfo(
            "Devolución registrada",
            f"Se devolvieron {unidades} unidades.\n"
            f"Valor registrado como salida de caja: {dinero(valor_reembolso)}."
        )

        modulo_devoluciones()

    tk.Button(
        formulario,
        text="Registrar devolución",
        command=registrar_devolucion,
        bg=VERDE_CLARO,
        fg=BLANCO,
        padx=15,
        pady=8
    ).pack(anchor="w", pady=12)


# ==========================================
# REPORTES
# ==========================================

def modulo_reportes():
    limpiar_contenido()
    titulo_pagina(
        "Reportes",
        "Resumen de los productos, las ventas y las devoluciones."
    )

    productos = cargar_productos()
    ventas = cargar_datos(ARCHIVO_VENTAS)
    devoluciones = cargar_datos(ARCHIVO_DEVOLUCIONES)

    total_ventas = sum(v["total"] for v in ventas)
    total_unidades = sum(p["stock"] for p in productos)
    total_devoluciones = sum(d["valor"] for d in devoluciones)

    datos = [
        ("Productos registrados", len(productos)),
        ("Unidades actuales", total_unidades),
        ("Ventas realizadas", len(ventas)),
        ("Valor de las ventas", dinero(total_ventas)),
        ("Devoluciones registradas", len(devoluciones)),
        ("Valor de las devoluciones", dinero(total_devoluciones))
    ]

    for etiqueta, valor in datos:
        fila = tk.Frame(
            contenido,
            bg=BLANCO,
            padx=15,
            pady=13
        )
        fila.pack(fill="x", pady=5)

        tk.Label(
            fila,
            text=etiqueta,
            bg=BLANCO,
            fg="#52645a",
            font=("Arial", 11)
        ).pack(side="left")

        tk.Label(
            fila,
            text=str(valor),
            bg=BLANCO,
            fg=VERDE,
            font=("Arial", 11, "bold")
        ).pack(side="right")


# ==========================================
# GESTIÓN DE CAJA
# ==========================================

def modulo_caja():
    limpiar_contenido()
    titulo_pagina(
        "Gestión de caja",
        "Registra entradas y salidas de dinero del supermercado."
    )

    movimientos = cargar_datos(ARCHIVO_CAJA)

    entradas_total = sum(
        m["valor"] for m in movimientos
        if m["tipo"] == "Entrada"
    )

    salidas_total = sum(
        m["valor"] for m in movimientos
        if m["tipo"] == "Salida"
    )

    saldo = entradas_total - salidas_total

    tk.Label(
        contenido,
        text=f"SALDO ACTUAL: {dinero(saldo)}",
        bg=BLANCO,
        fg=VERDE,
        font=("Arial", 21, "bold"),
        padx=20,
        pady=18
    ).pack(fill="x", pady=10)

    formulario = tk.LabelFrame(
        contenido,
        text="Registrar movimiento",
        bg=BLANCO,
        padx=15,
        pady=15
    )
    formulario.pack(fill="x", pady=12)

    tk.Label(
        formulario,
        text="Tipo de movimiento:",
        bg=BLANCO
    ).grid(row=0, column=0, padx=8, pady=8)

    tipo = ttk.Combobox(
        formulario,
        values=["Entrada", "Salida"],
        state="readonly",
        width=15
    )
    tipo.grid(row=0, column=1, padx=8, pady=8)
    tipo.set("Entrada")

    tk.Label(
        formulario,
        text="Concepto:",
        bg=BLANCO
    ).grid(row=1, column=0, padx=8, pady=8)

    concepto = tk.Entry(formulario, width=25)
    concepto.grid(row=1, column=1, padx=8, pady=8)

    tk.Label(
        formulario,
        text="Valor:",
        bg=BLANCO
    ).grid(row=2, column=0, padx=8, pady=8)

    valor = tk.Entry(formulario, width=25)
    valor.grid(row=2, column=1, padx=8, pady=8)

    def registrar_movimiento():
        clase = tipo.get()
        descripcion = concepto.get().strip()

        try:
            cantidad = float(valor.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "Ingresa un valor numérico mayor que cero."
            )
            return

        if not descripcion:
            messagebox.showwarning(
                "Atención",
                "Escribe el concepto del movimiento."
            )
            return

        movimientos_actuales = cargar_datos(ARCHIVO_CAJA)

        entradas = sum(
            m["valor"] for m in movimientos_actuales
            if m["tipo"] == "Entrada"
        )

        salidas = sum(
            m["valor"] for m in movimientos_actuales
            if m["tipo"] == "Salida"
        )

        saldo_actual = entradas - salidas

        if clase == "Salida" and cantidad > saldo_actual:
            messagebox.showerror(
                "Saldo insuficiente",
                "No hay suficiente dinero registrado en caja."
            )
            return

        movimientos_actuales.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": clase,
            "concepto": descripcion,
            "valor": cantidad
        })

        guardar_datos(ARCHIVO_CAJA, movimientos_actuales)

        messagebox.showinfo(
            "Correcto",
            "Movimiento registrado."
        )

        modulo_caja()

    tk.Button(
        formulario,
        text="Guardar movimiento",
        command=registrar_movimiento,
        bg=VERDE_CLARO,
        fg=BLANCO,
        padx=12,
        pady=7
    ).grid(row=3, column=1, pady=10)

    tk.Label(
        contenido,
        text="Movimientos de caja",
        bg=FONDO,
        fg=VERDE,
        font=("Arial", 15, "bold")
    ).pack(anchor="w", pady=8)

    tabla = crear_tabla(
        contenido,
        ("fecha", "tipo", "concepto", "valor"),
        ("Fecha", "Tipo", "Concepto", "Valor"),
        8
    )

    for movimiento in reversed(movimientos):
        tabla.insert(
            "",
            "end",
            values=(
                movimiento["fecha"],
                movimiento["tipo"],
                movimiento["concepto"],
                dinero(movimiento["valor"])
            )
        )




opciones = [
    ("Inicio", inicio),
    ("Gestión de productos", gestion_productos),
    ("Inventario", modulo_inventario),
    ("Realizar ventas", modulo_ventas),
    ("Facturación", modulo_facturacion),
    ("Devoluciones", modulo_devoluciones),
    ("Reportes", modulo_reportes),
    ("Gestión de caja", modulo_caja)
]

for texto, funcion in opciones:
    tk.Button(
        menu,
        text=texto,
        command=funcion,
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_CLARO,
        activeforeground=BLANCO,
        font=("Arial", 11),
        relief="flat",
        anchor="w",
        padx=18,
        pady=12
    ).pack(fill="x", padx=10, pady=3)

tk.Label(
    menu,
    text="Sistema de gestión\nMi Tienda © 2026",
    bg=VERDE,
    fg="#c4dfd0",
    font=("Arial", 10)
).pack(side="bottom", pady=20)



inicio()
ventana.mainloop()
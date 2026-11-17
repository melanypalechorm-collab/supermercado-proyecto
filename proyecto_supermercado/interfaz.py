import tkinter as tk
from tkinter import ttk, messagebox
import negocio

class SupermercadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Supermercado")
        self.root.geometry("800x600")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        self.crear_vista_catalogo()
        self.crear_vistas_pendientes('Punto de Venta')
        self.crear_vistas_pendientes('Inventario')
        self.crear_vistas_pendientes('Devoluciones')
        self.crear_vistas_pendientes('Caja')

    def crear_vista_catalogo(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Catálogo')
        
        ttk.Label(frame, text="Código:").grid(row=0, column=0, pady=5)
        self.e_cod = ttk.Entry(frame)
        self.e_cod.grid(row=0, column=1)
        
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, pady=5)
        self.e_nom = ttk.Entry(frame)
        self.e_nom.grid(row=1, column=1)
        
        ttk.Button(frame, text="Guardar", command=self.guardar).grid(row=2, column=0, columnspan=2, pady=10)

    def guardar(self):
        try:
            cod, nom = self.e_cod.get(), self.e_nom.get()
            if not cod or not nom: raise ValueError("Campos vacíos")
            negocio.registrar_producto(cod, nom, "Gen", 10, 15, 100, 10)
            messagebox.showinfo("Éxito", "Producto guardado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def crear_vistas_pendientes(self, nombre):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=nombre)
        ttk.Label(frame, text=f"Módulo {nombre} listo para desarrollo.").pack(pady=50)

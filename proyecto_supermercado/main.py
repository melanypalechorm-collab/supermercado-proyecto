import tkinter as tk
from interfaz import SupermercadoApp
import negocio

if __name__ == "__main__":
    negocio.inicializar()
    root = tk.Tk()
    app = SupermercadoApp(root)
    root.mainloop()

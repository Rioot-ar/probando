from tkinter import messagebox
import json
import os

class ProductoManager:
    JSON_FILE = "productos.json"

    def __init__(self):
        self.productos = self.cargar_productos()

    def cargar_productos(self):
        if os.path.exists(self.JSON_FILE):
            try:
                with open(self.JSON_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "El archivo de datos está corrupto. Se usará una lista vacía.")
        return []

    def guardar_productos(self):
        try:
            with open(self.JSON_FILE, "w") as file:
                json.dump(self.productos, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los datos: {e}")

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_productos()

    def editar_producto(self,producto):
        for i,product in enumerate(self.productos):
            if product["id"]==producto["id"]:
                self.productos[i] = producto
        self.guardar_productos()

    def eliminar_producto(self,id):
        for i,product in enumerate(self.productos):
            if product["id"]==id:
                del self.productos[i]
        self.guardar_productos()
from tkinter import filedialog, messagebox
from ProductFrame import ProductoFrame
import customtkinter as ctk
import tkinter as tk
from ProductManager import ProductoManager


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Productos")
        self.configure(fg_color=("#febeac","#010A26"))
        x = (self.winfo_screenwidth() // 2) - (1360 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1360x800+{x}+{y}")
        self.resizable(False,False)
        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", self.buscar_productos)

        self.entry = ctk.CTkEntry(self, textvariable=self.entry_var,font=ctk.CTkFont(family="Times", size=25),height=50)
        self.entry.pack(side="top", fill="x", padx=50, pady=10)

        self.manager = ProductoManager()
        self.product_frame = ProductoFrame(self, self.manager)
        self.product_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.crear_menu()
        self.product_frame.cargar_productos()

    def buscar_productos(self,*args):
        filtro = self.entry.get()
        if(len(filtro)>=3):
            self.product_frame.mostrar_productos(filtro)
            self.product_frame._scrollbar._command('moveto', 0)
        elif(len(filtro)==0):
            self.product_frame.mostrar_productos()
    
    
    def crear_menu(self):
        menu_bar = tk.Menu(self)

        menu_archivo = tk.Menu(menu_bar, tearoff=0)
        menu_temas = tk.Menu(menu_bar, tearoff=0)

        menu_archivo.add_command(label="Agregar Producto", command=self.agregar_producto)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)

        menu_temas.add_command(label="Claro", command=self.cambiar_tema_light)
        menu_temas.add_command(label="Oscuro", command=self.cambiar_tema_dark)

        menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_bar.add_cascade(label="Tema", menu=menu_temas)
        self.configure(menu=menu_bar)

    def cambiar_tema_light(self):
        ctk.set_appearance_mode("light")
    def cambiar_tema_dark(self):
        ctk.set_appearance_mode("dark")

    def agregar_producto(self):
        def guardar_producto():
            nombre = entry_nombre.get()
            precio = entry_precio.get()
            stock = entry_stock.get()
            imagen = entry_imagen.get()

            if not (nombre and precio and stock and imagen):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            if not self.manager.productos:
                nuevo_id = 1 
            else:
                nuevo_id = max(producto["id"] for producto in self.manager.productos) + 1

            self.manager.agregar_producto({"id":nuevo_id , "nombre": nombre, "precio": precio, "stock": stock, "imagen": imagen})
            self.product_frame.agregar_producto({"id":nuevo_id , "nombre": nombre, "precio": precio, "stock": stock, "imagen": imagen},self.entry.get())
            ventana_agregar.destroy()
            messagebox.showinfo("Éxito", "Producto agregado exitosamente")

            
        def seleccionar_imagen(entry):
            ruta = filedialog.askopenfilename(initialdir="imagenes",filetypes=[("Archivos de imagen", ("*.png","*.jpg","*.jpeg"))])
            if (ruta.find("imagenes")==-1):
                messagebox.showerror("Error", "Las imagenes deben estar en imagenes/")
                return
            ruta = ruta[ruta.find("imagenes"):]
            entry.delete(0, tk.END)
            entry.insert(0, ruta)
            
            
        
        ventana_agregar = ctk.CTkToplevel(self)
        ventana_agregar.title("Agregar Producto")
        ventana_agregar.geometry("400x400")
        ventana_agregar.transient(self)

        ctk.CTkLabel(ventana_agregar, text="Nombre:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana_agregar)
        entry_nombre.pack(pady=5,padx=50, fill="x")

        ctk.CTkLabel(ventana_agregar, text="Precio:").pack(pady=5)
        entry_precio = ctk.CTkEntry(ventana_agregar)
        entry_precio.pack(pady=5,padx=50, fill="x")

        ctk.CTkLabel(ventana_agregar, text="Stock:").pack(pady=5)
        entry_stock = ctk.CTkEntry(ventana_agregar)
        entry_stock.pack(pady=5,padx=50, fill="x")

        ctk.CTkLabel(ventana_agregar, text="Ruta de imagen:").pack(pady=5)
        frame_imagen = ctk.CTkFrame(ventana_agregar)
        frame_imagen.pack(pady=5, fill="x")
        entry_imagen = ctk.CTkEntry(frame_imagen)
        entry_imagen.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(frame_imagen, text="Seleccionar", command=lambda: seleccionar_imagen(entry_imagen)).pack(side="right", padx=5)

        ctk.CTkButton(ventana_agregar, text="Guardar", command=guardar_producto).pack(pady=20)
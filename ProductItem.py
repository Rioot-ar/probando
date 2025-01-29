from tkinter import filedialog, messagebox
import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image

class ProductItem(ctk.CTkFrame):
    def __init__(self, parent, producto):
        super().__init__(parent,border_width=1,fg_color=("#96b5a6","#30588C"))
        self.id, self.nombre, self.precio, self.stock, self.ruta_imagen = producto.values()
        self.parent=parent
        self.fila=0
        self.columna=0
        self.carga_item()

        

    def carga_item(self):
        try:
            img = Image.open(self.ruta_imagen)
            my_image = ctk.CTkImage(light_image=img, dark_image=img,size=(200, 200))

            self.image_label = ctk.CTkLabel(self, image=my_image, text="")
            self.image_label.pack()
        except Exception as e:
            print(e)
            self.image_label = ctk.CTkLabel(self, text="Sin imagen",text_color="black",width=200,height=200)
            self.image_label.pack(pady=5)

        if(len(self.nombre)>32):
            self.nombreLabel=ctk.CTkLabel(self, text=self.nombre[0:36], font=("Arial", 20, "bold"),text_color=("#000000","#FFFFFF"),height=55,wraplength=200)
            self.nombreLabel.pack()
        else:
            self.nombreLabel=ctk.CTkLabel(self, text=self.nombre, font=("Arial", 20, "bold"),height=55,text_color=("#000000","#FFFFFF"),wraplength=200)
            self.nombreLabel.pack()       
                
        self.precioLabel=ctk.CTkLabel(self, text=f"${self.precio}", font=("Arial", 20),text_color=("#000000","#FFFFFF"))
        self.precioLabel.pack()

        self.stock_frame = ctk.CTkFrame(self,fg_color=("#96b5a6","#30588C"))
        self.stock_frame.pack(pady=5)

        ctk.CTkButton(self.stock_frame, text="-", width=30 ,command=self.disminuir_stock,fg_color=("#fce1cb","#091740"),text_color=("#000000","#FFFFFF")).pack(side="left", padx=5)
        self.stockLabel=ctk.CTkLabel(self.stock_frame, text=f"Stock: {self.stock}", font=("Arial", 15))
        self.stockLabel.pack(side="left")
        ctk.CTkButton(self.stock_frame, text="+",width=30, command=self.aumentar_stock,fg_color=("#fce1cb","#091740"),text_color=("#000000","#FFFFFF")).pack(side="left", padx=5)        

        ctk.CTkButton(self, text="Editar",width=20, command=self.editar_producto,fg_color=("#fce1cb","#091740"),text_color=("#000000","#FFFFFF")).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(self, text="Eliminar",width=20, command=self.eliminar_producto,fg_color=("#fce1cb","#091740"),text_color=("#000000","#FFFFFF")).pack(side="right", padx=5, pady=5)
    
    def dibujar_item(self,fila,columna):
        self.fila=fila
        self.columna=columna
        self.grid(row=fila, column=columna, padx=10, pady=10)
        
    

    def update(self):
        try:
            img = Image.open(self.ruta_imagen)
            my_image = ctk.CTkImage(light_image=img, dark_image=img,size=(200, 200))

            self.image_label.configure(self, image=my_image, text="")
        except:
            self.image_label.configure(self, text="Sin imagen",text_color="black",width=200,height=200)
        if(len(self.nombre)>32):
            self.nombreLabel.configure(self, text=self.nombre[0:36], font=("Arial", 20, "bold"),text_color=("#000000","#FFFFFF"),height=55,wraplength=200)
        else:
            self.nombreLabel.configure(self, text=self.nombre, font=("Arial", 20, "bold"),height=55,text_color=("#000000","#FFFFFF"),wraplength=200)

        self.precioLabel.configure(self, text=f"${self.precio}", font=("Arial", 20),text_color=("#000000","#FFFFFF"))
        self.stockLabel.configure(self.stock_frame, text=f"Stock: {self.stock}", font=("Arial", 15))

    def disminuir_stock(self):
        if int(self.stock) > 0:
            self.stock = str(int(self.stock) - 1)
            self.update()
            self.parent.manager.editar_producto({"id":self.id, "nombre": self.nombre, "precio": self.precio, "stock": self.stock, "imagen": self.ruta_imagen})

    def aumentar_stock(self):
        self.stock = str(int(self.stock) + 1)
        self.update()
        self.parent.manager.editar_producto({"id":self.id, "nombre": self.nombre, "precio": self.precio, "stock": self.stock, "imagen": self.ruta_imagen})

    def editar_producto(self):
        
        def guardar_producto():
            self.nombre = entry_nombre.get()
            self.precio = entry_precio.get()
            self.stock = entry_stock.get()
            self.ruta_imagen = entry_ruta_imagen.get()
            
            if not (self.nombre and self.precio and self.stock and self.ruta_imagen):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            self.update()
            self.parent.manager.editar_producto({"id":self.id, "nombre": self.nombre, "precio": self.precio, "stock": self.stock, "imagen": self.ruta_imagen})

            ventana_editar.destroy()
            messagebox.showinfo("Éxito", "Producto agregado exitosamente")

        def seleccionar_imagen(entry):
            ruta = filedialog.askopenfilename(initialdir="imagenes",filetypes=[("Archivos de imagen", ("*.png","*.jpg","*.jpeg"))])
            if (ruta.find("imagenes")==-1):
                messagebox.showerror("Error", "Las imagenes deben estar en imagenes/")
                return
            ruta = ruta[ruta.find("imagenes"):]
            entry.delete(0, tk.END)
            entry.insert(0, ruta)
        
        ventana_editar = ctk.CTkToplevel(self)
        ventana_editar.title("Editar Producto")
        ventana_editar.geometry("400x400")
        ventana_editar.transient(self)

        ctk.CTkLabel(ventana_editar, text="Nombre:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana_editar)
        entry_nombre.insert(0, self.nombre)
        entry_nombre.pack(pady=5,padx=50, fill="x")

        ctk.CTkLabel(ventana_editar, text="Precio:").pack(pady=5)
        entry_precio = ctk.CTkEntry(ventana_editar)
        entry_precio.insert(0, self.precio)
        entry_precio.pack(pady=5,padx=50, fill="x")

        ctk.CTkLabel(ventana_editar, text="Stock:").pack(pady=5)
        entry_stock = ctk.CTkEntry(ventana_editar)
        entry_stock.insert(0, self.stock)
        entry_stock.pack(pady=5,padx=50, fill="x")

        ctk.CTkLabel(ventana_editar, text="Ruta de imagen:").pack(pady=5)
        frame_imagen = ctk.CTkFrame(ventana_editar)
        frame_imagen.pack(pady=5, fill="x")
        entry_ruta_imagen = ctk.CTkEntry(frame_imagen)
        entry_ruta_imagen.insert(0, self.ruta_imagen)
        entry_ruta_imagen.pack(side="left", fill="x", expand=True, padx=5)
        btn_imagen = ctk.CTkButton(frame_imagen, text="Seleccionar", command=lambda: seleccionar_imagen(entry_ruta_imagen))
        btn_imagen.pack(side="right", padx=5)

        ctk.CTkButton(ventana_editar, text="Guardar Cambios", command=guardar_producto).pack(pady=20)

    def eliminar_producto(self):
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?"):
            self.parent.manager.eliminar_producto(self.id)
            self.parent.eliminar_producto(self.id)
            self.destroy()
            self.parent.mostrar_productos()
from ProductItem import ProductItem
import customtkinter as ctk


class ProductoFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, manager):
        super().__init__(parent,width=parent._current_width, height=parent._current_height,fg_color=("#febeac","#010A26"))
        self.manager = manager
        self.parent=parent
        self.productItems=[]

        self.cargar_productos
        self.mostrar_productos

        self.pack()


    def cargar_productos(self, filtro=""):
        fila, columna = 0, 0
        columnas = 6
        self.productItems.clear()
        for i,producto in enumerate(self.manager.productos):
            id, nombre, precio, stock, ruta_imagen = producto.values()
            if filtro.lower() in nombre.lower():
                self.productItems.append(ProductItem(self,producto))
                self.productItems[i].dibujar_item(fila,columna)
                columna += 1
                if columna == columnas:
                    columna = 0
                    fila += 1

    def agregar_producto(self,producto,filtro):
        self.productItems.append(ProductItem(self,producto))
        self.mostrar_productos(filtro)
    
    def eliminar_producto(self,id):
        for i, producto in enumerate(self.productItems):
            if producto.id == id:
                del self.productItems[i]
        

    def mostrar_productos(self,filtro=""):
        for widget in self.winfo_children():
            widget.grid_remove()
        fila, columna = 0, 0
        columnas = 6
        #quien te conoce encapsulamiento
        for i,producto in enumerate(self.productItems):
            if filtro.lower() in self.productItems[i].nombre.lower():
                self.productItems[i].dibujar_item(fila,columna)
                
                columna += 1
                if columna == columnas:
                    columna = 0
                    fila += 1

        
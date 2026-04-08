import tkinter as tk
from ventana_principal import VentanaPrincipal
from PIL import Image, ImageTk
from explorador import crear_explorador

class AppPrincipal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CreaGUIPy")

        # PANTALLA COMPLETA
        self.root.state("zoomed")

        self.crear_menu()

        # CONTENEDOR DINÁMICO
        self.contador_archivos = 0
         
        # CONTENEDOR PRINCIPAL
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # PANEL IZQUIERDO (EXPLORADOR)
        self.panel_izq = tk.Frame(self.main_frame, width=200)
        self.panel_izq.pack(side="left", fill="y")

        self.lista_archivos = crear_explorador(self.panel_izq)

        # PANEL DERECHO (ÁREA DE TRABAJO)
        self.area_trabajo = tk.Frame(self.main_frame)
        self.area_trabajo.pack(side="right", fill="both", expand=True)      # MOSTRAR FONDO CON LOGO
        self.mostrar_fondo()

    # =========================
    # MENÚ SUPERIOR
    # =========================
    def crear_menu(self):

        menu_bar = tk.Menu(self.root)

        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.abrir_disenador)
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

        self.root.config(menu=menu_bar)

    def mostrar_fondo(self):

        imagen = Image.open("imagenes/marcade_agua.png").convert("RGBA")

        # Ajustar a pantalla
        imagen = imagen.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        )

        #Opacidad 50%
        alpha = imagen.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.5))
        imagen.putalpha(alpha)

        self.img_tk = ImageTk.PhotoImage(imagen)

        self.label_fondo = tk.Label(self.area_trabajo, image=self.img_tk)
        self.label_fondo.place(relwidth=1, relheight=1)
    # =========================
    # CAMBIAR VISTA
    # =========================
    def limpiar_contenido_central(self):
        for widget in self.area_trabajo.winfo_children():
            widget.destroy()

    def abrir_disenador(self):

        self.contador_archivos += 1
        nombre_archivo = f"archivo_{self.contador_archivos}.py"

        self.lista_archivos.insert(tk.END, nombre_archivo)

        # eliminar fondo
        self.limpiar_contenido_central()

        # cargar diseñador (reemplaza TODO el área)
        self.ventana = VentanaPrincipal(self.area_trabajo)
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppPrincipal()
    app.run()
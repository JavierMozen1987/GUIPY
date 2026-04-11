import tkinter as tk
from tkinter import messagebox
from ventana_principal import VentanaPrincipal
from PIL import Image, ImageTk
from explorador import crear_explorador
import os


class AppPrincipal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CreaGUIPy")
        self.root.state("zoomed")

        self.contador_archivos = 0
        self.ventana = None

        self.crear_menu()

        # CONTENEDOR PRINCIPAL
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # PANEL IZQUIERDO (EXPLORADOR)
        self.panel_izq = tk.Frame(self.main_frame, width=200)
        self.panel_izq.pack(side="left", fill="y")

        self.lista_archivos = crear_explorador(self.panel_izq)

        # PANEL DERECHO (ÁREA DE TRABAJO)
        self.area_trabajo = tk.Frame(self.main_frame)
        self.area_trabajo.pack(side="right", fill="both", expand=True)

        # MOSTRAR FONDO CON LOGO
        self.mostrar_fondo()

    # =========================
    # MENÚ SUPERIOR
    # =========================
    def crear_menu(self):
        menu_bar = tk.Menu(self.root)

        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.abrir_disenador)
        archivo_menu.add_command(label="Guardar archivo", command=self.guardar_codigo_python)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        self.root.config(menu=menu_bar)

    # =========================
    # FONDO
    # =========================
    def mostrar_fondo(self):
        try:
            ruta_base = os.path.dirname(__file__)
            ruta_imagen = os.path.join(ruta_base, "imagenes", "marcade_agua.png")

            imagen = Image.open(ruta_imagen).convert("RGBA")
            imagen = imagen.resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            )

            alpha = imagen.split()[3]
            alpha = alpha.point(lambda p: int(p * 0.8))
            imagen.putalpha(alpha)

            self.img_tk = ImageTk.PhotoImage(imagen)

            self.label_fondo = tk.Label(self.area_trabajo, image=self.img_tk)
            self.label_fondo.place(relwidth=1, relheight=1)

        except Exception as e:
            # Si no encuentra la imagen, no detiene el programa
            self.label_fondo = tk.Label(
                self.area_trabajo,
                text="CreaGUIPy",
                font=("Arial", 28, "bold"),
                fg="gray"
            )
            self.label_fondo.place(relx=0.5, rely=0.5, anchor="center")
            print(f"No se pudo cargar la imagen de fondo: {e}")

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

        # cargar diseñador
        self.ventana = VentanaPrincipal(self.area_trabajo)

    # =========================
    # GUARDAR ARCHIVO
    # =========================
    def guardar_codigo_python(self):
        if self.ventana is None:
            messagebox.showwarning("Aviso", "Primero debes crear un archivo nuevo.")
            return

        try:
            self.ventana.guardar_codigo_python()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppPrincipal()
    app.run()
    
